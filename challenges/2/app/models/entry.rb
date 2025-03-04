class Entry < ApplicationRecord
  belongs_to :vault

  validates :title, :username, :password, presence: true
end
