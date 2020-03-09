# Easy Schedule User Manual

[![GitHub license](https://img.shields.io/badge/license-GPL3.0-blue.svg)](https://github.com/NaiveWang/DirtRallyTelemetry/blob/master/LICENSE)

a multi-user scheduling website.

This project is implemented with `SQLite` and `Python Flask`. This readme is also a help page of the website itself. Base64 encoding is used for obfuscating database to provide better user privacy.

To deploy the peroject, clone this repository and follow instructions [here](https://github.com/NaiveWang/easy_schedule/blob/master/deploy.md).

## User Base

This website is not designed for massive deployed project due to SQLite DB. As a result, unlimited sign-up is not permitted and not avalible. Instead, an activation transation is implemented.

### Activation

A new user is set by administrator with an activation code, then new user should be invited with this activation code.

For new user: open the [activation page](/activate), input your new user name, passcode and your given activation code to activate your account.

If you have been redirect to login page, your activation was successful.

### Login

[this page](/login) to login.

## Navigation

Usage of this website. Please notice all the pages are redirected to login page until you have got the login session.

### [Credit](/)

User's home page.

### [Me](/me)

You can change your wassup and passwd and your visibility to public(feed) here.

#### Invite Friend

In `Me` Section, user could generate friend code to be other user's friend. Once user click the generate button, an `uuid` code was set and is avaliable to share. Also, once a code is filled by other user, it would have been got expired. Adding a friend is asymmetric since if `a` have invited `b` successfully, `a` is a friend of `b` but not vice versa, say, `b` have to invite `a` successlly if and only if `b` has became a friend of `a`.

Accepting a friend invitation is easy: fill the `Friend Code` and click `Add Friend`. Adding user itself as a friend is rejected with `narcissistic rejection` and repeatedly adding user who has been a friend will only void the code.

A `collision avoidance` logic is added to `code generating` transation. As a result, user can get no code after the `code generating` operation and another try is needed. Collision is merely happened but feasible ([detail](https://en.wikipedia.org/wiki/Universally_unique_identifier#Collisions)).

### [Hub](/hub)

To peek other users' progress and wassup. Current version shows all the public content of proof and visible users.

### [Manage](/manage)

The user management sestion is about deletion of `Todo(s)`, `Credit(s)`, `Friend(s)` and `PoW`. It took two steps of deletion, first mark as trash then user can delete or recover from trash. Only `Friend(s)` is without protection.

### [Log out](/logout)

To logout and leave the page

### HELP

This is where you are now.

## [Credit System](/)

User could add goal with some credit for motivation. The credit is avaliable only if it reaches user's holding credit. Credits could be arranged with `dependencies (prerequisites)`.

There are four sestions of Credit, `Avaliable` section lists what you can afford; `inprogress` section lists when *money (credits) is the only problem*; `Pending` section lists no items avaliable even they are cheap enough; and `Finished` section list what you have spent.

### Create

Find the [link](/new_credit) under Credit, fill name and price of it. User can set current credit avaliable after (s)he have spent some credit (Adding Prerequisite).

### Spend

After you click the followed **spend** button, you can do what credit permitted. Notice there is no rollback, be careful.

## To-do

`Todo` is the core function of this platform. User can add new `todo` and proof work of it. `Todo` has many types like `book`, which is a kind of `todo` dediceted to some textbook stuff. A dependency could be assigned to `new todo` as a prerequisite, which you can proof your work of it when the dependency (prerequisite) is finished. User could choose their `friend` as their instructor, then the `todo` need to be proofed by the `friend` instead. Users who have created the `todo` always earn their credits. Todo have four rows: `ToDo`, `Instructed`, `Pending` and `Finished`; for `what you are working with`, `what you are being instructed`, `what you cannot work with yet` and `what you have done`.

### [Book type](/todo_book)

#### new

To create a todo of type book, click [new](/new_todo?tid=1) under the `book section`, type `book name`, `starting page` and `ending page`. The `rate` represents how much credit you will earn for each page, it is set to 1 by default to indicate earning 1 credit per page. Of course, this `book` model is not restrict to *book* itself, it could also be used as some countable and atomic jobs like beat 100 medium leetcode problems.

#### proof

When you have gone through some pages, you can click "`proof`" right of your book `ToDo` stash to proof what you have just read. Ending page is set to 1 page incremental by default, and it can be set higher. You need to fill proof row about what you have learned or anything you can recall. Take it seriously since a short pause can boost your later progress. You have choose the option of posting to public or it will not shows at other users' `Hub` page.
