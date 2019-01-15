# coding: utf-8
#/usr/bin/ruby
require 'nokogiri'
require 'httparty'
require 'base64'

target = ARGV[0]
year   = ARGV[1]
URL = ENV['ROK_REQUEST_URL']
soldiers_selector = "#searchTable > tbody > tr"

(1..12).each do |month|
  _month = (month / 10).to_s + (month % 10).to_s
  (1..31).each do |day|
    _day = (day / 10).to_s + (day % 10).to_s
      
    birthday         = year + _month + _day
    encoded_target   = Base64.encode64(target)
    encoded_birthday = Base64.encode64(birthday)
    query = {
      "search%3Asearch_key1%3Achild_search" => "etc_char8",
      "search%3Asearch_key2%3Achild_search" => "etc_char9",
      "search%3Asearch_key3%3Achild_search" => "etc_char1",
      "search_val1" => encoded_target,
      "search_val2" => encoded_birthday,
      "birthDay" => birthday,
      "search_val3" => "Name"          
    }

    response = HTTParty.post(URL, :body => query)
    html = Nokogiri::HTML(response)
    puts("-----------------------------------")
    puts("Entrance Date #{target}, Birth Date #{birthday} : ")
    puts("-----------------------------------")
    
    solider_list = html.css(soldiers_selector)
    if solider_list.size == 0
      puts "NO ENTRY"
    else
      solider_list.each do |soldier|
        puts soldier.text
      end
    end
    sleep(0.2)
  end
end


