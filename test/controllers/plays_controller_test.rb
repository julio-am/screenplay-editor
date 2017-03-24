require 'test_helper'

class PlaysControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get plays_index_url
    assert_response :success
  end

  test "should get reader" do
    get plays_reader_url
    assert_response :success
  end

end
