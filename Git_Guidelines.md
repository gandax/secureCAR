# 1 Commit Messages

## 1.1 Title and description
    
- First line: Tag in all caps, followed by a brief description (~ 50 characters)
- Second line: blank
- Following lines: more detailed description, line-wrapped at 72 characters. May contain multiple paragraphs, separated by blank lines.

## 1.2 Tense

Use the present tense when writing messages, i.e. "Fix bug, apply patch", not "Fixed bug, applied patch".

## 1.3 Tags

***[ADD]*** 	: When you add a new file   
***[REMOVE]*** 	: When you remove a file   
***[FIX]*** 	: When you fix a bug   
***[REFACT]*** 	: When you simply modify a file organization, do an indentation, ... (Make a file more readable)   
***[MOVE]*** 	: When you move a part of the code to an other file or when you subdivise functions   
***[UPDATE]*** 	: When you update a file (add functions, code, ...)   

> When you need to use a FIX or MOVE tag, describe why you had to do that in the commit description.

# 2 Basic Git commands

## 2.1 Clone

If you just want to try the project or just get a stable version, clone the branch ***master*** 
```bash
git clone https://github.com/gandax/secureCar.git
```

If you want to contribute to the project, clone the branch ***dev***
```bash
git clone -b dev https://github.com/gandax/secureCar.git
```

## 2.2 Keep your fork up to date

```bash
cd into/cloned/fork-repo
git remote add upstream git://github.com/ORIGINAL-DEV-USERNAME/REPO-YOU-FORKED-FROM.git
git fetch upstream

git pull upstream yourBranch
```

## 2.3 add, commit, push

```bash
git status
```
You can view the status of all files a have modified since the last commit.

```bash
git add [file]
```
This tells git that the file(s) should be added to the next commit. You'll need to do this on files you modify, also.

```bash
git commit [file]
```
Commit your changes locally.

```bash
git commit -a
```
> If you want to commit all the files you have changed without making the add command for each.

```bash
git push origin your_branch
```
This command pushes the current state of your local repository, including all commits, up to github. Your work becomes part of the history of the your_branch branch on github.

```bash
git push 
```
This is the command that changes the state of the remote code branch. 

> Nothing you do locally will have any affect outside your workstation until you push your changes.

