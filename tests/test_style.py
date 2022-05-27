import requests, tarfile, os
from subprocess import check_output, CalledProcessError


script_path = "./game.sh"

def download_shellcheck():
    link = "https://github.com/koalaman/shellcheck/releases/download/v0.8.0/shellcheck-v0.8.0.darwin.x86_64.tar.xz"

    r = requests.get(link, allow_redirects=True)
    fname = 'shellcheck-v0.8.0.darwin.x86_64.tar.xz'
    open(fname, 'wb').write(r.content)
    tar = tarfile.open(fname, "r:xz")

    for member in tar.getmembers():
        if member.isreg() and member.name.endswith('shellcheck'):
            member.name = os.path.basename(member.name) # remove the path by reset it
    tar.extract(member,'.') # extrac
    tar.close()
    return "./shellcheck"

binary_path = download_shellcheck()

def run_shell_test(script, arg1):
    out = check_output([script, str(arg1)], universal_newlines=True)
    return out.split("\n")[0]

def test_shellcheck():
    #result = run_shell_test(script_path, '1,2,3,4,5,6,7')
    failed = False
    try:
        result = run_shell_test(binary_path, script_path)
    except CalledProcessError as e:
        failed = True
        result = e.output
    print(result)
    assert failed == False