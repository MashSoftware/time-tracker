# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/MashSoftware/time-tracker/compare/main...develop)

## [0.29.0](https://github.com/MashSoftware/time-tracker/compare/v0.28.3...v0.29.0) - 2023-10-30

### Added

- Dark mode. There is no light mode. This is the way.

### Changed

- Cancel button on time entry forms now goes back to the referring page with url query strings, instead of the latest weekly page.
- Next page navigation button is removed on the current week page.
- Previous page navigation button is removed on the 12th week page, as per the users time entry history limit.
- Tests follow redirects to login page where authentication is required.

### Fixed

- Radios not populating when editing an existing time entry or setting a default tag/location.

## [0.28.3](https://github.com/MashSoftware/time-tracker/compare/v0.28.2...v0.28.3) - 2023-10-25

### Fixed

- Heroku Postgres dialect difference
- Updated SQLAlchemy UUID types cast as Strings

## [0.28.2](https://github.com/MashSoftware/time-tracker/compare/v0.28.1...v0.28.2) - 2023-10-24

### Changed

- Local development now uses Docker and Docker Compose. Thanks [@ahosgood](https://github.com/ahosgood).
- Publish Docker image to GitHub Packages.
- Upgraded requirements.
- Bump Python version to 3.11.6.

### Fixed

- Add timeout to external API HTTP requests.

## [0.28.1](https://github.com/MashSoftware/time-tracker/compare/v0.28.0...v0.28.1) - 2022-08-13

### Changed

- Upgraded requirements
- Bump Python version to 3.10.6

### Fixed

- Error on account activation due to trying to log the current user when not signed in.
- Incorrect link URL to GitHub releases page.

## [0.28.0](https://github.com/MashSoftware/time-tracker/compare/v0.27.0...v0.28.0) - 2022-08-12

### Added

- Custom locations can be created and added to time entries, allowing tracking of working from multiple places.
- New URL: [time-tracker.mashsoftware.com](https://time-tracker.mashsoftware.com).
- Aria labels on icons where needed, i.e. where used decoratively without additional text.
- More meta keywords for better search engine indexing.

### Changed

- Renamed application from "The Button" to "Mash Time Tracker", following a new naming convention for Mash Software projects.
- Redesigned home page highlighting main features of the app and secondary technical features.
- Application now doesn't go to sleep after a period of inactivity.
- Actions on cards (entries, tags and locations) now appear in a card footer.
- Increased gap between block level buttons in mobile widths for easier tap targets.

### Fixed

- Time entries recorded on Sundays were saved and accounted for in totals, but not displayed in the weekly view. Thanks [@ahosgood](https://github.com/ahosgood).

## [0.27.0](https://github.com/MashSoftware/time-tracker/compare/v0.26.0...v0.27.0) - 2022-08-04

### Added

- Cookie page detailing what cookies the app uses and the ability to accept or reject non-essential cookies. Link also added to footer.
- Cookie banner to allow users to accept or reject non-essential cookies.
- Persistent `cookies_policy` cookie is set to store preferences with an expiry of one year.
- App-wide CSRF protection. All forms were already CRSF protected using WTForms, but this setting protects every route unless explicitly exempt.
- Highlight active navigation item in navbar.
- Development-only requirements containing packages used for linting, formatting, testing and requirements management.
- Using Pytest Coverage to measure unit test coverage, including in branching code.
- Refactored unit and functional tests. Thanks [@jonodrew](https://github.com/jonodrew).
- Error handling if email send request to service providers API fails for any reason. Re-raised as a 500 internal server error and logged.
- Error pages contain a back link taking the user back to the referring page if there was one.

### Changed

- Time entries spanning multiple days now add the date to the end time e.g. instead of _"22:00 to 06:00"_ it's now _"22:00 to 28/03/2021 06:00"_.
- "Remember me" checkbox is removed from the login page if the user has not accepted non-essential cookies.
- `session` and `remember_token` cookies are set to `HttpOnly` and `Secure` to prevent access over non-HTTPS connections or via JavaScript to mitigate cookie theft via cross-site scripting (XSS) or eavesdropping.
- Reduced `remember_token` cookie expiration from one year, to thirty days.
- Content Security Policy (CSP) updated to require HTTPS connection to all sources.
- Require a fresh login (not a restored session) prior to any delete action.
- CSRF errors are now explicitly handled with a flash message to inform the user to try again, rather than a form validation error.
- Flash messages have been simplified to three categories; error, important and success. Error messages are used for form validation and are not dismissable. Important and success messages are dismissable contextual confirmation of user actions.
- Form fields validation error messages are now added to the `aria-describedby` attribute.
- Non-primary action buttons now use the "outline" style.
- Footer layout redesigned for multiple columns on desktop and single column on mobile.
- Reduce header content margin.
- Swapped Fontawesome icons out for Bootstrap icons
- Upgraded to Bootstrap v5.2.0

### Removed

- Python 3.6 support
- Postgres 10 support
- Redis 5 support

### Fixed

- Prevent other users time entries from appearing in search results. Other users entries could not be edited or deleted, this resulted in a 403 forbidden error.
- Pre-select "None" when changing default tag and user has no tags.
- Database URI using deprecated scheme designator.

## [0.26.0](https://github.com/MashSoftware/time-tracker/compare/v0.25.0...v0.26.0) - 2021-03-09

### Added

- Search for time entries based on comment contents.
- Set a default tag to use for all new time entries created with the "Start now" button. Thanks [@ahosgood](https://github.com/ahosgood).
- Use webmanifest shortcuts to expose start / stop now function to OS. Thanks [@andymantell](https://github.com/andymantell).
- Better logging to `stdout` and `stderr` to aid app monitoring.
- More unit tests.
- Versioning, contributors, support to the [README](README.md)
- [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md)
- [Contribution guidelines](CONTRIBUTING.md)

### Changed

- Pre-select users default tag, or "None" if not set, on manual time entry form.
- Tag page highlights which tag is the current default.

### Fixed

- Pre-select "None" tag when editing and existing entry if no tag was previously selected. Thanks [@ahosgood](https://github.com/ahosgood).
- Prevent viewing other users tagged time entries pages if you knew the UUID of the tag.

## [0.25.0](https://github.com/MashSoftware/time-tracker/compare/v0.24.0...v0.25.0) - 2021-02-26

### Added

- Scheduled task to delete all time entries older than 12 weeks. This is run daily at midnight UTC and based on the start date and time of the time entry. This helps to minimise the storage requirements of the app.
- Display time entry history retention period and date in user account page.
- Total amount of time associated with each tag on both the tag list page and tagged time entry pages.
- Date a tag was last used displayed on tag card.

### Changed

- Time entry limit changed to entry history retention period in account settings.
- Weekly summary now includes the current duration of in-progress time entries in both time and tag totals.
- Redesigned home page and re-written selling-points.
- Redesigned page title headers.
- Redesigned layout of tag card.
- Moved more code to common utils with additional unit tests.

### Removed

- User account based limit of 120 entries. Now you can create as many time entries as you like, but they will be deleted after 12 weeks.

## [0.24.0](https://github.com/MashSoftware/time-tracker/compare/v0.23.2...v0.24.0) - 2021-01-19

### Added

- New tagged entry page showing all time entries linked to a particular tag.
- In-progress time entry cards now have a header that displays how long ago that entry started (on page load/refresh, not real-time). Thanks [@ahosgood](https://github.com/ahosgood).
- Count of time entries and tags used vs limits on the account page.

### Changed

- Tag page layout now shows tags alongside the number of times each has been used, link to view all time entries linked to that tag and links to edit or delete.
- Tags on time entry cards are now links to the new tagged time entries page showing all entries with that tag.
- Delete tag page now says how many time entries will be impacted, with a link to view them before confirming or cancelling the delete action.
- Removed italic (emphasis) from time entry comments so that emojis don't look weird.
- Improved 404 error pages where URL pattern matches the expected type, but is not a valid instance of that type.
- Removed drop-down from "Stop now" button since all items on it are disabled anyway. Now only show dropdown on the "Start now" button state. Thanks [@andymantell](https://github.com/andymantell).
- Delete account confirmation page now says how many entries and tags will be deleted along with the account.

### Fixed

- Tag names containing only whitespace now fail form validation, must contain some other characters.
- Strip whitespace before checking for duplicated tag names.
- Strip whitespace before creating or editing a tag name.

## [0.23.2](https://github.com/MashSoftware/time-tracker/compare/v0.23.1...v0.23.2) - 2021-01-03

### Added

- Unit test to cover verification token generation bug found in previous release.

### Changed

- Renamed default branch from `master` to `main` and renamed all references.

### Fixed

- Error when requesting activation for unregistered email addresses.
- Whitespace not stripped from comments, resulting in empty strings stored instead of null.

## [0.23.1](https://github.com/MashSoftware/time-tracker/compare/v0.23.0...v0.23.1) - 2021-01-01

### Fixed

- Verification token not generated correctly preventing user sign up or password reset confirmation emails from being sent.

## [0.23.0](https://github.com/MashSoftware/time-tracker/compare/v0.22.0...v0.23.0) - 2020-12-31

### [Blog](https://medium.com/mash-software/time-tracker-weekly-summaries-comments-and-ui-upgrade-d543945069d4)

### Added

- Weekly summary card displaying total of time entries and progress against scheduled time, along with total time per tag used.
- Comments of up to 64 characters can be added to new or existing time entries.
- Automated unit test suite for bespoke (non-framework/package related) and common code.
- Set up [GitHub Actions](https://github.com/features/actions) CI/CD workflow to check dependencies are up-to-date, run code quality linting and automated unit tests prior to deployment.
- Improved new user experience with pointers to create tags and set time schedule if an account has none.
- Added unique ID to each time card, allowing for URI fragment linking within the entries page.
- Provide positive feedback for successfully validated form fields on submit.

### Changed

- Updated to Bootstrap v5 Beta 1 now that new features and breaking changes have stabalised. This encompasses a large number of UI changes required to upgrade.
- Moved progress bar from above time entry cards to below the "Start now" button, within the new weekly summary card.
- Refactored repeated code into common utilities module and replaced all instances with calls to a singular methods.
- Refactored time card template to include actions block where appropriate, reducing repeated code and increasing ease of change.
- On desktop device widths buttons will space out horizontally, dropping to vertically stacked block buttons on mobile device widths.

### Removed

- Removed JQuery since it is no longer required by Bootstrap v5.

### Fixed

- Decimal hours calculation to display non-rounded floating point numbers, to two decimal places. Durations are no longer rounded, so 59 minutes and 59 seconds is represented correctly as 0.99 decimal hours, not rounded to 1.0.

## [0.22.0](https://github.com/MashSoftware/time-tracker/compare/v0.21.1...v0.22.0) - 2020-11-28

### [Blog](https://medium.com/mash-software/time-tracker-weekly-view-time-schedules-begining-beta-2cb451df5cff)

### Added

- Weekly time entry view, showing time entries recorded in a specific week, along with a progress indicator of time recorded against scheduled weekly hours.
- Manage scheduled working time per day in account settings. Used to calcuate weekly hours and track progress. Will also be used for future daily time credit/debit features.
- Start tagged time entries immediately using the dropdown button menu
- Open Graph Protocol metadata tags to enable better link sharing on social media.
- ARIA attributes added to help text within forms, to improve accessibility and assistive technology user experience.

### Changed

- Moving into [beta](https://en.wikipedia.org/wiki/Software_release_life_cycle#Beta) after 14 releases during 18 months in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha).
- Improved email address validation on sign up, log in, password reset, account activation and account update. Now provides more granular error messages if an input email address is invalid. Also checks the deliverability of the email address by resolving the domain name.
- Delete confirmation actions changed from modal dialogs to new pages, inspired by [this tweet](https://twitter.com/adambsilver/status/1290266510334681088).
- Increased user tag limit from 5 to 8.
- Consistent actions, headings and confirmation messages.
- Upgrade to Bootstrap 4.5.3.
- Increased rate limit to allow for more user requests per second before hitting an error page.

### Fixed

- Bug in conversion between timestamps stored as UTC and displayed in the users selected timezone when editing an existing time entry.

## [0.21.1](https://github.com/MashSoftware/time-tracker/compare/v0.21.0...v0.21.1) - 2020-02-25

### Fixed

- Large pagination controls did not fit on mobile display widths. Reverted to standard size.

## [0.21.0](https://github.com/MashSoftware/time-tracker/compare/v0.20.0...v0.21.0) - 2020-02-25

### [Blog](https://medium.com/mash-software/time-tracker-native-controls-app-icons-and-performance-bbafad029257)

### Added

- Favicons, Apple touch icons, Android Chrome icons and Windows 8/10 tile icons. Thanks [@joehonywill](https://github.com/joehonywill)

### Changed

- Use HTML5 input types for dates and times, to instruct browsers to present their own controls where available. On mobile devices the native date and time picker controls will be used. This gives users an easier, quicker and more familiar way to input information.
- Use Bootstrap's custom form controls to provide consistency between browsers and a more cohesive look and feel.
- Updated design of account page.
- Upgrade to Bootstrap 4.4.1.
- Accessibility and best practice fixes from Google Lighthouse analysis.

## [0.20.0](https://github.com/MashSoftware/time-tracker/compare/v0.19.0...v0.20.0) - 2019-08-08

### [Blog](https://medium.com/mash-software/time-tracker-time-tags-e1979d2a0556)

### Added

- Create and maintain a set of up to five tags, used to categorise time entries.
- Edit a time entry to select from your personal list of tags to apply.
- Display tags on cards in the time entry view.
- Help topics relating to tags.

## [0.19.0](https://github.com/MashSoftware/time-tracker/compare/v0.18.0...v0.19.0) - 2019-07-25

### Added

- Version number and release date added to page footer, with a link to this changelog.
- For all pages with a primary action button, a secondary "cancel" button has been added.

### Changed

- Large refactor to modularise application code, in preparation for new features.
- Moved time entries to their own URL on `/entries` along with top navigation bar link.
- Updated help page with categories questions and answers.
- Reverted secondary action buttons to non-outline styling, since they were visually too close to a form input field.

## [0.18.0](https://github.com/MashSoftware/time-tracker/compare/v0.17.0...v0.18.0) - 2019-07-11

### [Blog](https://medium.com/mash-software/introducing-time-tracker-aef549dacfbf)

### Added

- Time entry duration expressed as time and decimal hours.
- Daily total time duration expressed as time and decimal hours.
- A limit of 80 time entries per account.
- Tell the user when they have reached the limit on their account.
- The users oldest entry is deleted when creating a new one, once the account entry limit has been reached.
- Help page with FAQs.

### Changed

- Landing page sales pitch describing the service.
- Wording on link to resend account activation email.
- If a user requests another activation email and they have never activated before, they will receive the original activation email. Otherwise they will receive the confirmation email used when changing email address.

## [0.17.0](https://github.com/MashSoftware/time-tracker/compare/v0.16.0...v0.17.0) - 2019-06-18

### Added

- New accounts must be activated to confirm the email address used is genuine and accessible by the user.
- Send an activation token to the users email address.
- Activation timestamp is recorded on users account information.
- Accounts that have not been activated are not able to log in.
- Activation request form for users whose tokens expire or are not received.
- Changing the email address on an account then requires that new email address to be confirmed. An email is sent to the new address after change.
- Flash message if an invalid or expired password reset token is provided, informing the user to request another.

### Changed

- Generic user token generation and verification methods.
- Improved wording in password reset email content.
- Disabled browser spellchecking on email address input fields.
- Set maximum length of email addresses to 256 characters, validated by forms.
- Enabled browser autocompletion of email address fields.
- Display email address to the user to confirm email sending actions.

## [0.16.0](https://github.com/MashSoftware/time-tracker/compare/v0.15.0...v0.16.0) - 2019-06-13

### Added

- HTTP security headers via [Talisman](https://github.com/GoogleCloudPlatform/flask-talisman), gaining an [A+ rating](https://securityheaders.com/?q=https%3A%2F%2Fmash-time-tracker.herokuapp.com%2F&followRedirects=on).
- Defined Content Security Policy. Thanks [@andymantell](https://github.com/andymantell).
- Ability to request a password reset from the login page. Thanks [@skipster2k2](https://github.com/skipster2k2).
- Send a reset password email via [Mailgun](https://www.mailgun.com) to the user with a unique URL containing a JSON Web Token (JWT) that can be decoded to the user's ID.
- Form to allow the user to change their password once a valid password reset token has been supplied.
- Links to GitHub diffs for each release in changelog.
- Thanks to anyone who helped in any way with an item in each release.

### Changed

- All non-primary actions are now outline buttons, to promote the visual hierarchy of the primary action.
- On the "Edit time entry" form, the primary action is now "Save" instead of "Edit".
- Refactored URLs to remove reference to `push` resource in favour of `entry` for consistency of language.
- Dropped `/update` from the update entry URL since there is no non-updaing view of the resource.

## [0.15.0](https://github.com/MashSoftware/time-tracker/compare/v0.14.1...v0.15.0) - 2019-05-24

### Changed

- Redesigned time cards using list groups within cards. One card per day, many entry pairs per card. List items are clickable links to edit that entry.
- Given greater visual identification to in-progress time entries, highlighting with the "info" contextual class and added wording.
- Removed seconds from time card display to improve readability. Thanks [@LlamaComedian](https://github.com/LlamaComedian).

## [0.14.1](https://github.com/MashSoftware/time-tracker/compare/v0.14.0...v0.14.1) - 2019-05-22

### Fixed

- "Start/stop" button displayed the wrong text for new users with no entries, now corrected. Thanks [@russwillis](https://github.com/russwillis).
- An unsuccessful login attempt hit the rate limiter due to the redirect to the same page, added a 1 second sleep to overcome.
- Spacing between the new split button and the first date entry on mobile was a little close, added some padding.

## [0.14.0](https://github.com/MashSoftware/time-tracker/compare/v0.13.0...v0.14.0) - 2019-05-21

### Added

- Pagination of time entries, with 10 per page.
- Controls to navigate paginated time entries.
- Manual time entry form, accessible via dropdown on split start/stop button. Thanks [@annie-birchall](https://github.com/annie-birchall).

## [0.13.0](https://github.com/MashSoftware/time-tracker/compare/v0.12.0...v0.13.0) - 2019-05-17

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

## [0.12.0](https://github.com/MashSoftware/time-tracker/compare/v0.11.0...v0.12.0) - 2019-05-14

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

## [0.11.0](https://github.com/MashSoftware/time-tracker/compare/v0.10.1...v0.11.0) - 2019-05-07

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

- Editing times in Chrome resulted in an error due to the `datetime-local` picker tool removing seconds. Changed inputs to `text` type rather than HTML5 `datetime-local` to improve compatibility at the expense of browser/device native pickers. Needs further investigation to improve user experience. Thanks [@mattgirdler](https://github.com/mattgirdler).

## [0.10.1](https://github.com/MashSoftware/time-tracker/compare/v0.10.0...v0.10.1) - 2019-05-01

### Fixed

- User account dates and times missing localisation

## [0.10.0](https://github.com/MashSoftware/time-tracker/compare/v0.9.0...v0.10.0) - 2019-05-01

### Added

- Display locale aware dates and times. Thanks [@annie-birchall](https://github.com/annie-birchall).
- HTTP Exception handling
- Footer links
- Alpha phase badge in nav bar
- Address bar theme colour

### Fixed

- Raise Forbidden (403) exception when attempting to edit or delete time entries not belonging to the current user

## [0.9.0](https://github.com/MashSoftware/time-tracker/compare/v0.8.0...v0.9.0) - 2019-04-26

### Added

- Delete time entries
- Edit time entries

## [0.8.0](https://github.com/MashSoftware/time-tracker/compare/v0.7.0...v0.8.0) - 2019-04-24

### Added

- Update account details

### Changed

- Sign up or log in links in homepage text

## [0.7.0](https://github.com/MashSoftware/time-tracker/compare/v0.6.0...v0.7.0) - 2019-04-24

### Added

- Change password for user account

### Changed

- Include sub-template for events

## [0.6.0](https://github.com/MashSoftware/time-tracker/compare/v0.5.0...v0.6.0) - 2019-04-23

### Removed

- User first name and last name

## [0.5.0](https://github.com/MashSoftware/time-tracker/compare/v0.4.0...v0.5.0) - 2019-04-23

### Added

- "The button" to add events
- List of start and stop timestamps
- Public homepage for non-signed in users

### Changed

- Consistent datetime formatting
- Updated meta tags

## [0.4.0](https://github.com/MashSoftware/time-tracker/compare/v0.3.0...v0.4.0) - 2019-04-18

### Added

- Delete user account

## [0.3.0](https://github.com/MashSoftware/time-tracker/compare/v0.2.0...v0.3.0) - 2019-04-18

### Added

- User account page
- Record time user last logged in
- Redirect protection after log in

## [0.2.0](https://github.com/MashSoftware/time-tracker/compare/v0.1.0...v0.2.0) - 2019-04-18

### Added

- User log in
- User log out

### Changed

- Navigation based on authentication status
- Flash message formatting

## [0.1.0](https://github.com/MashSoftware/time-tracker/compare/4b9057c8b8b4d110496dfabf9dd31b9e86070d4a...v0.1.0) - 2019-04-18

### Added

- Basic application setup
- User sign up
- Form validation
