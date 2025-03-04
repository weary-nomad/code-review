class VaultsController < ApplicationController
  before_action :require_login

  def index
    @vaults = current_user.vaults
  end

  def show
    @vault = current_user.vaults.find(params[:id])
    @entries = @vault.entries
  end

  def new
    @vault = Vault.new
  end

  def create
    @vault = current_user.vaults.build(vault_params)
    if @vault.save
      redirect_to @vault
    else
      render :new
    end
  end

  private

  def vault_params
    params.require(:vault).permit(:name)
  end

  def require_login
    unless current_user
      flash[:alert] = 'You must be logged in'
      redirect_to login_path
    end
  end

  def current_user
    @current_user ||= User.find(session[:user_id]) if session[:user_id]
  end
end
