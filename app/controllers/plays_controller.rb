require 'nokogiri'
class PlaysController < ApplicationController
  def index
    document = Nokogiri::XML.parse(File.open('app/views/plays/data.xml')) 
    body = document.xpath("//xmlns:body")
    acts = body.children
    @array = Array.new
    for scenesAndActHead in acts
        if checkTag(scenesAndActHead, @array)
            for stageDirsAndSceneHead in scenesAndActHead
                if checkTag(stageDirsAndSceneHead, @array)
                    for speaker in stageDirsAndSceneHead
                        if checkTag(speaker, @array)
                            @array = getlines(speaker, @array)
                        end
                    end
                end
            end
        end
    end
  end

  def checkTag (node, array)
    if (node.matches?('head') || node.matches?('stage') || node.matches?('speaker'))
        array.push(node.inner_text)
        return false
    return true
    end
  end

  def getlines(node, array)
    string = ""
    for child in node.children
        if child.matches?('milestone')
            array.push(string)
            string = ""
        else
            string += child.inner_text
        end
    end
    return array
  end

  def reader
  end

end
