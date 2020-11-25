# Telegram Spammer
Telegram spammer is a tool helps you in spam and other thing in telegram.

# نصب
After you cloned the repository install needed libraries.

```bash
pip3 install -r requirements.txt
```

After installing libraries go to [My Telegram Website](https://my.telegram.org/auth) and login. then go to `API Development` and fill the fields and create your app.

Then create **config.ini** file and replace your values:

```ini
[auth]
api_id = Your API ID
api_hash = Your API Hash
client_count = Your Accounts Count

[client0]
phone = Your Phone Number
name = Name

.....
```

# Usage

Run program.

```bash
python3 main.py
```

program has different commands

*Simple commands:*

| command | description           |
| ------- | --------------------- |
| exit    | Exit from program     |
| clear   | Clear the screen      |
| history | Show commands history |
| banner  | Show banner           |
| help    | Show commands help    |

**Note:** You can use TAB for completion
**Note2:** Use the following commands for more information:

```bash
help command
```
یا
```bash
command -h
```

## Send text messages

First create a file and write messages you want to send.

Then use this command to send messages.

```bash
sendtext -f file [-c count] target
```

> target: Your Target  
> -f file: File name that you created  
> -c count: The number of messages you intend to send (Optional)

## Join/Leave chat or channel

```bash
join ChatID ClientNumber [-p]
```

> ChatID: That chat or channel you want to join  
> ClientNumber: That client you want to joins chat  
> -p: If chat is private use this option. (Optional)

```bash
leave ChatID ClientNumber
```

> ChatID: That chat or channel you want to leave  
> ClientNumber: That client you want to leaves chat  

# Contribute
Apply to participate in this project through pull requests or send a message to my ID in Telegram.

# Donate
Bitcoin: 1GKiThh6AaAj8Y1TEbwgC6cvrD82UyWDFk
