Use a python virtual environment to run this app on your local system

## Steps to intall npm and angular cli in virtual environment ##
1. First ensure that you have python virtualenv installed.
(If not, run `pip install virtualenv` )

2. Create a new virtual environment using the following command in this directory.
`virtualenv myenvname`

3. cd into 'myenvname'

4. Activate your virtual environment
`.\Scripts\activate` in windows
`./Scripts/activate` in Linux or Mac

5. Install npm for virtualenv
`pip install nodeenv`
`nodeenv -p`

6. Install angular cli using npm package manager
`npm install -g @angular/cli`

7. Run this to deactivate your virtual environment
`deactivate`