import os, shutil

package_directory = "package"
os.chdir(package_directory)

while True:
    answer = input(
'''1: install library
2: uninstall library
3: build
4: upload to pypi.org
5: run test.py here
6: run test.py on CMD
7: install from file
> ''')

    if answer == '1':
        os.system("pip install chromaconsole -U")
    elif answer == '2':
        os.system("pip uninstall chromaconsole")
    elif answer == '3':
        if os.path.isdir('dist'):
            shutil.rmtree('dist')
        os.system("py -m build")
    elif answer == '4':
        os.system("py -m twine upload --repository pypi dist/*")
        os.system("py -m twine upload --repository testpypi dist/*")
    elif answer == '5':
        os.system("py ../test.py")
    elif answer == '6':
        os.system(f'start cmd /k python ../test.py')
    elif answer == '7':
        os.system("pip install .")
    else:
        print("Invalid choice. Please select a valid option.")