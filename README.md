<p align="center">
	<h1 align="center">☁️ Autosave Submod ☁️</h1>
	<h3 align="center">Fully automatic persistent backups to Github (so far)</h3>
</p>

<p align="center">
	<a href="https://github.com/friends-of-monika/mas-autosave/releases/latest">
		<img alt="Latest release" src="https://img.shields.io/github/v/release/friends-of-monika/mas-autosave">
	</a>
	<a href="https://github.com/friends-of-monika/mas-autosave/releases">
		<img alt="Release downloads" src="https://img.shields.io/github/downloads/friends-of-monika/mas-autosave/total">
	</a>
	<a href="https://github.com/friends-of-monika/mas-autosave/blob/main/LICENSE.txt">
		<img alt="MIT license badge" src="https://img.shields.io/github/license/friends-of-monika/mas-autosave">
	</a>
	<a href="https://mon.icu/discord">
		<img alt="Discord server" src="https://discordapp.com/api/guilds/1029849988953546802/widget.png?style=shield">
	</a>
	<a href="https://ko-fi.com/Y8Y15BC52">
		<img alt="Ko-fi badge" src="https://ko-fi.com/img/githubbutton_sm.svg" height="20">
	</a>
</p>

## 🌟 Features

* Convenient and easy-to-figure-out settings UI
* Fully automatic backups without your interaction
  - Support for periodic backups as well as backup on 'Goodbye'

<!-- If you want to show off screenshots, you can put them in 'doc/screenshots'
	and reference them here. This is basically an HTML table with two columns. -->
<!-- ## 🖼️ Screenshots

<details>
	<summary>Click here to see all screenshots...</summary>
	<table>
		<tr>
			<td><img src="doc/screenshots/Screenshot0.png" alt="GUI example"></td>
			<td><img src="doc/screenshots/Screenshot1.png" alt="Topics overview"></td>
		</tr>
		<tr>
			<td><img src="doc/screenshots/Screenshot2.png" alt="Speech saving"></td>
			<td><img src="doc/screenshots/Screenshot3.png" alt="Generating topic"></td>
		</tr>
	</table>
</details> -->

## ❓ Installing

1. Go to [the latest release page](https://github.com/friends-of-monika/mas-autosave)
   and scroll to Assets section.
2. Download `autosave-VERSION.zip` file.
3. Drag and drop `Submods` folder from it into your `game` folder.
4. You're all set!~

## 🔧 Configuring

### 📦 Github

> [!NOTE]
> At the moment, only Github backend is supported. In future more options may be available.

First setup of Autosave submod may be a little tricky, but if you follow this guide it'll be
piece of cake!~ 🍰

1. Log in or sign up at Github. In this guide, we're assuming you're on desktop 💻

2. Click on plus button at the top, and click on 'New repository'
   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_repo_1.png)
   ![Screenshot 2](doc/ghsetup_repo_2.png)

   </details>

3. Here, enter any desired name (`monika-autosaves` is a good example), and set it as private

   *Your persistent contains all Monika's memories about you &mdash; including private info too.
   Keep your persistent safe &mdash; make your repository private 🛡️*

   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_repo_3.png)

   </details>

4. Go to your settings &mdash; click on your avatar in the top corner, then on 'Settings'
   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_token_1.png)
   ![Screenshot 2](doc/ghsetup_token_2.png)

   </details>

5. Look to the left, and scroll all the way to the bottom of the menu &mdash; you'll need
   the section labelled 'Developer settings'
   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_token_3.png)

   </details>

6. Now, click on 'Personal access tokens' section to unfold it, then on 'Fine-grained tokens'
   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_token_4.png)
   ![Screenshot 2](doc/ghsetup_token_5.png)

   </details>

7. Click on 'Generate new token' button

   *You may be asked to enter your password or authorize with 2FA here &mdash; do so if asked*

   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_token_6.png)

   </details>

8. Type anything you like in the 'Token name' field &mdash; it only serves as a label for you;
   next up, select 'No expiration' under 'Expiration' field &mdash; so that you won't have to
   renew this API token again in future
   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_token_7.png)

   </details>

   Further on, scroll down to 'Repository access' section; here, click on 'Only select repositories', and select your previously created repository from the list
   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_token_8.png)
   ![Screenshot 2](doc/ghsetup_token_9.png)

   </details>

   Then scroll down to 'Permissions' section; click on it to unfold, find
   'Contents' section and set it to 'Read and write'
   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_token_10.png)
   ![Screenshot 2](doc/ghsetup_token_11.png)
   ![Screenshot 3](doc/ghsetup_token_12.png)

   </details>

   Almost there &mdash; scroll until you see 'Generate token' button and press it, then copy the token using 'copy' button
   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_token_13.png)
   ![Screenshot 2](doc/ghsetup_token_14.png)

   </details>

   Github stuff is behind us now &mdash; let's set up Autosave submod in game 🎉

9. Open Submods menu in settings, and click on 'API Keys' section on the left
   <details>
   <summary>Click here to see screenshots</summary>

   ![Screenshot 1](doc/ghsetup_mas_1.png)

   </details>

10. Find '\[Autosave\] Github API token' field, and click 'Paste'
    <details>
    <summary>Click here to see screenshots</summary>

    ![Screenshot 1](doc/ghsetup_mas_2.png)
    ![Screenshot 1](doc/ghsetup_mas_3.png)

    </details>

11. Open 'Submods' section on the left, and find 'Autosave' submod in the list &mdash; then, click 'Select repository' and select your repository from earlier steps
    <details>
    <summary>Click here to see screenshots</summary>

    ![Screenshot 1](doc/ghsetup_mas_4.png)
    ![Screenshot 2](doc/ghsetup_mas_5.png)

    </details>

12. You're all set! 🥳 You can check that it works by clicking 'Force save'
    and saving your persistent.
    <details>
    <summary>Click here to see screenshots</summary>

    ![Screenshot 1](doc/ghsetup_mas_6.png)
    ![Screenshot 2](doc/ghsetup_mas_7.png)

    </details>


## 💬 Join our Discord

We're up to chat! Join our Discord server [here](https://mon.icu/discord).

[![Discord server invitation](https://discordapp.com/api/guilds/1029849988953546802/widget.png?style=banner3)](https://mon.icu/discord)
