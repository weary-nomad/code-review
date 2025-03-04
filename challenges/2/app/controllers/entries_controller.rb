class EntriesController < ApplicationController
  before_action :require_login

  def create
    @vault = current_user.vaults.find(params[:vault_id])
    @entry = @vault.entries.build(entry_params)
    if @entry.save
      redirect_to vault_path(@vault)
    else
      render 'vaults/show'
    end
  end

  def update
    @entry = Entry.find(params[:id])
    if @entry.update(entry_params)
      redirect_to vault_path(@entry.vault)
    else
      render 'vaults/show'
    end
  end

  def destroy
    @entry = Entry.find(params[:id])
    @entry.destroy
    redirect_to vault_path(@entry.vault)
  end

  private

  def entry_params
    params.require(:entry).permit(:title, :username, :password, :notes)
  end
end
