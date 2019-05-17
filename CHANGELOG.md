# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.13.0] - 2019-05-17

### Added

- Require fresh login in order to update account details, change password or delete account.
- Rate limiting backed by Redis.
- Global rate limits of 1 per second and 60 per minute for all unauthenticated requests, based on remote IP address.
- Specific rate limits of 1 per second for authenticated requests to account and time related actions, based on user ID.
- Enabled gzip compression.

### Changed

- Strip whitespace from around template tags to reduce the size of output html pages.

### Fixed

- Fixed an error that occurred when editing a time entry with no end timestamp due to null timezone conversion.

## [0.12.0] - 2019-05-14

### Added

- Capture user selected time zone on sign up.
- Update time zone in account details.

### Changed

- Timezones and conversions are now handled server-side based on the users selected timezone in their account.
- Existing accounts have a default UTC timezone until set by the user.
- All primary action buttons are now larger than non-primary actions, to help the user identify the intended action to take.
- All buttons are now block sized, to improve hit target on mobile devices and for consistency on all devices.
- Reduced responsive breakpoint for forms so fields don't render full page width on iPad sized devices.

### Removed

- Removed Flask Moment (and therefore MomentJS) in favour of server-side timezone handling.
- Removed approximate time since started for in-progress entries.
- Removed "Go back" button on forms, since this just replicates browser back in most cases.
- Removed stopwatch icon from start/stop button.

### Fixed

- Updating account details and _not_ changing email address generated a validation error, because the email address is already in use. Now if the email address is not changed no validation error occurrs.
- Fixed error when trying to localise a non-existant timestamp for accounts that have never been updated.

## [0.11.0] - 2019-05-07

### Added

- Display approximate time since started for in-progress entries
- Auto refresh time since started every minute

### Changed

- Simplified time entry card layout
- Using 24 hour time format
- Grouped entries by start date
- Moved delete time entry button from card to edit page to prevent accidental deletions
- Handle times that span dates by showing the end date and time
- Added icon and "now" to the button to make it clear the action relates to the current time

### Fixed

- Editing times in Chrome resulted in an error due to the `datetime-local` picker tool removing seconds. Changed inputs to `text` type rather than HTML5 `datetime-local` to improve compatibility at the expense of browser/device native pickers. Needs further investigation to improve user experience.

## [0.10.1] - 2019-05-01

### Fixed

- User account dates and times missing localisation

## [0.10.0] - 2019-05-01

### Added

- Display locale aware dates and times
- HTTP Exception handling
- Footer links
- Alpha phase badge in nav bar
- Address bar theme colour

### Fixed

- Raise Forbidden (403) exception when attempting to edit or delete time entries not belonging to the current user

## [0.9.0] - 2019-04-26

### Added

- Delete time entries
- Edit time entries

## [0.8.0] - 2019-04-24

### Added

- Update account details

### Changed

- Sign up or log in links in homepage text

## [0.7.0] - 2019-04-24

### Added

- Change password for user account

### Changed

- Include sub-template for events

## [0.6.0] - 2019-04-23

### Removed

- User first name and last name

## [0.5.0] - 2019-04-23

### Added

- "The button" to add events
- List of start and stop timestamps
- Public homepage for non-signed in users

### Changed

- Consistent datetime formatting
- Updated meta tags

## [0.4.0] - 2019-04-18

### Added

- Delete user account

## [0.3.0] - 2019-04-18

### Added

- User account page
- Record time user last logged in
- Redirect protection after log in

## [0.2.0] - 2019-04-18

### Added

- User log in
- User log out

### Changed

- Navigation based on authentication status
- Flash message formatting

## [0.1.0] - 2019-04-18

### Added

- Basic application setup
- User sign up
- Form validation