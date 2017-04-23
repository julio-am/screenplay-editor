Rails.application.routes.draw do
  get 'plays/characters'

  get 'plays/index'

  root 'plays#index'
  resources :plays

  get 'plays/reader'

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
