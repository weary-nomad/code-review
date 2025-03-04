Rails.application.routes.draw do
  root 'sessions#new'

  get '/login', to: 'sessions#new', as: 'login'
  post '/login', to: 'sessions#create'
  delete '/logout', to: 'sessions#destroy'
  
  resources :vaults do
    resources :entries, only: [:create, :update, :destroy]
  end
end
