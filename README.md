# SFAS-final-project

# Git setup:
    First we need to set git's global configuration settings
    Type in the terminal:
        git config --global user.name "NAME" 
        git config --global user.email "email" 

    Then we need to add an SSH key to your git hub.
        Follow the following guide. When you are asked to create a password you can just click ENTER to leave the password blank.
        https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

    Now we clone the repository to our computer. 
        In github click the green button that says "code" 
        select SSH
        copy the link.

        navigate to your hello_ros folder
        type in terminal:
            mkdir final_project
            cd final_project
            git clone <link from github> .

        Now the folder should contain the contents of the repository.

        Some useful commands:
            git status  # shows the status of your local folder. Use this liberally
            git add .   # adds all untracked files (that are not in the .gitignore) to be tracked by the repository
            git commit -a -m "commit message"   # commits all changes. Try to write useful messages to explain what you changed.
            git push    # pushes your changes to the cloud
            git pull    # retrieves commits from the cloud and merges them into your local branch
            git fetch   # retrieves commits from the cloud without merging the into your local branch 
            git merge   # merges your local branch with master
            git log     # see log of commits.
            
# add a path.py file to your final_project folder containing the following code
    PATH = "<path to your catkin workspace>"

# general outline of python modules
    write functions that contains does the actions we need done and can be called from the main script.
    Try (if possible) to have the functions work only on the data passed to the functions and then return the result.

    use:
        if __name__ == '__main__':
    
    To create test code that runs only if the module is run directely and not called from the main script.







