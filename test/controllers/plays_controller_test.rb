require 'test_helper'

class PlaysControllerTest < ActionDispatch::IntegrationTest
  test "should get characters" do
    get plays_characters_url
    assert_response :success
  end

  test "should get index" do
    get plays_index_url
    assert_response :success
  end

end
