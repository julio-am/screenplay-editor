require 'nokogiri'
class PlaysController < ApplicationController
  def index
    document = Nokogiri::XML.parse(File.open('app/views/plays/data.xml')) 
    @body = document.xpath("//xmlns:body")
    @firstLevel = @body.children
  end

  def reader
  end
end
