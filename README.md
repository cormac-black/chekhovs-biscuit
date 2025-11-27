# chekhovs-biscuit

Chekhov's Biscuit is a testing ground for getting acclimated with github and moving files around. 

How to push a file to a repo?

cd to the directory

if the directory does not exist on the local computer, go the PWD where the folder will be created:

    clone the repository folder

      in the example of this repo, <git clone https://github.com/cormac-black/chekhovs-biscuit.git>

      cd into the repo on the local computer

check the connection:

    git remote -v

    >> <address> (fetch)
    >> <address> (push)

IMPORTANT Before adding, sychronize  to be sure your not overriding any changes:

    git pull origin main

    >> Already up to date

cp files into local repo directory

    git add file1.txt. file2.txt 

check the status:

    git status 

    >> should show the files to be added in green (these files are staged for a 'push')

commit the files, it's like a snapshot all the changes made to the branch, because what is on your repo is going to become what is on the origin repo, you also type up a summary of the changes.

    git commit -m "uploading file1.txt and file.txt"

Finally you push all the changes to the origin repo.

    git  push origin main
 
Oh, and make my funk the P funk... I wants to get funked up.
