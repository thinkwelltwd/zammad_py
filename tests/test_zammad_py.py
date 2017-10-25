#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `zammad_py` package."""
from conftest import zammad_vcr


class TestAPI:

    @zammad_vcr.use_cassette(
        'tests/fixtures/zammad_users.yml', record_mode='new_episodes'
    )
    def test_users(self, zammad_api):
        all_users = zammad_api.user.all()
        assert all_users[-1]['id'] == 3
        assert all_users[-1]['firstname'] == 'Joe'

        current_user = zammad_api.user.me()
        assert current_user['id'] == 3
        assert current_user['firstname'] == 'Joe'

        current_user = zammad_api.user.find(3)
        assert current_user['id'] == 3
        assert current_user['firstname'] == 'Joe'

        new_user = zammad_api.user.create({
            'firstname': 'TestUser',
            'lastname': 'LastName'
        })
        assert new_user['id'] == 5
        assert new_user['firstname'] == 'TestUser'

        updated_user = zammad_api.user.update(5, {'firstname': 'TestUser1'})
        assert updated_user['firstname'] == 'TestUser1'

        deleted_user = zammad_api.user.destroy(5)
        assert deleted_user == dict()

        current_user, = zammad_api.user.search({'query': 'Joe'})
        assert current_user['id'] == 3

    @zammad_vcr.use_cassette(
        'tests/fixtures/zammad_tickets.yml', record_mode='new_episodes'
    )
    def test_tickets(self, zammad_api):
        all_tickets = zammad_api.ticket.all()
        assert all_tickets[0]['id'] == 1
        assert all_tickets[0]['title'] == 'Welcome to Zammad!'

        current_ticket = zammad_api.ticket.find(1)
        assert current_ticket['id'] == 1
        assert current_ticket['title'] == 'Welcome to Zammad!'

        new_ticket = zammad_api.ticket.create({
            'title': 'some new title',
            'state': 'new',
            'priority': '2 normal',
            'owner': '-',
            'customer': 'nicole.braun@zammad.org',
            'group': 'Users',
            'article': {
                'sender': 'Customer',
                'type': 'note',
                'subject': 'some subject',
                'content_type': 'text/plain',
                'body': "some body\nnext line",
            }
        })
        assert new_ticket['title'] == 'some new title'
        assert new_ticket['customer'] == 'nicole.braun@zammad.org'

        updated_ticket = zammad_api.ticket.update(6, {'title': 'TestTicket1'})
        assert updated_ticket['title'] == 'TestTicket1'

        deleted_ticket = zammad_api.ticket.destroy(6)
        assert deleted_ticket == ''

        current_ticket = zammad_api.ticket.search({
            'query': 'Ticket 1'
        })
        assert current_ticket['tickets'] == [2]

    @zammad_vcr.use_cassette(
        'tests/fixtures/zammad_groups.yml', record_mode='new_episodes'
    )
    def test_groups(self, zammad_api):
        all_groups = zammad_api.group.all()
        assert all_groups[0]['id'] == 1
        assert all_groups[0]['note'] == 'Standard Group/Pool for Tickets.'

        current_group = zammad_api.group.find(1)
        assert current_group['id'] == 1
        assert current_group['note'] == 'Standard Group/Pool for Tickets.'

        new_group = zammad_api.group.create({
            'name': 'Name1',
            'note': 'note1'
        })
        assert new_group['name'] == 'Name1'
        assert new_group['note'] == 'note1'

        updated_group = zammad_api.group.update(2, {'name': 'Name2'})
        assert updated_group['name'] == 'Name2'

        deleted_group = zammad_api.group.destroy(2)
        assert deleted_group == dict()
