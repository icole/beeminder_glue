require 'pry'
require 'capybara'
require 'capybara/poltergeist'
require 'net/http'

module DataquestScraper
  extend Capybara::DSL
  Capybara.default_driver = :poltergeist
  # Return a hash of each track name w/ progress %
  def self.run
    url = "https://www.dataquest.io/profiles/#{ENV['DATAQUEST_USERNAME']}"
    visit url
    sleep 1
    tracks = {}
    all('div.track-progress').each do |track|
      track_progress = track.text.match(/([\d]*)%/).to_s
      track_name = track.text.gsub(" #{track_progress}", "")
      tracks[track_name] = track_progress.gsub('%', '').to_i
    end
    return tracks
  end
end

class Beeminder
  class << self
    def sync_goal_with(goal, value = 0)
      raise 'Beeminder Auth Token not set.' unless ENV['BEEMINDER_AUTH_TOKEN']
      raise 'Beeminder Username not set' unless ENV['BEEMINDER_USERNAME']

      @auth_token = ENV['BEEMINDER_AUTH_TOKEN']
      @username = ENV['BEEMINDER_USERNAME']
      @goal = goal
      if datapoint_changed value
        create_datapoint value
      end
    end

    def beeminder_url
      "https://www.beeminder.com/api/v1/users/#{@username}/goals/#{@goal}/datapoints.json?auth_token=#{@auth_token}"
    end

    def create_datapoint value
      puts "Update goal (#{@goal}) to: #{value}"
      Net::HTTP::post_form URI(beeminder_url), value: value
    end

    def datapoint_changed value
      begin
        last_datapoint = JSON.parse(Net::HTTP::get URI(beeminder_url))[0]['value'].to_i
        puts "Current goal value is: #{last_datapoint}"
        value > last_datapoint
      rescue Exception => boom
        raise "Datapoint check failed with: #{boom}"
      end
    end
  end
end

track_progress = DataquestScraper.run
Beeminder.sync_goal_with("dataquest", track_progress['Data analyst'])
