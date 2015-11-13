#!/bin/sh -e

rootdir=$(git rev-parse --show-toplevel)
cd $rootdir

if [ -f .ruby-version ]; then
	RUBY_VER=$(cat .ruby-version)
fi

test -f /etc/debian_version && PATCH="https://bugs.ruby-lang.org/attachments/download/5479/ruby-sslv3.diff"

if [ ! -z $RUBY_VER ]; then
	if [ x"$(rbenv version | awk '{print $1}')" != x"$RUBY_VER" ]; then
		if ! rbenv versions | grep -wq "$RUBY_VER"; then
			if [ -z $PATCH ]; then
				rbenv install $RUBY_VER
			else
				curl -fsSL $PATCH | rbenv install --patch $RUBY_VER
			fi
		fi
	fi
	rbenv local $RUBY_VER
	rbenv rehash
fi

rbenv exec gem list | grep -wq bundler || rbenv exec gem install bundler

bundle install --path vendor/bundle

bundle exec rake spec

exit 0
