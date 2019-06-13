#!/usr/bin/env python3
import sys, re

DEFAULT_PRINTS = [
    "remote"
]

TEMPLATE_ITEMS = None

def get_info(opts):
    if TEMPLATE_ITEMS is not None and "info" not in opts:
        return

    with open(__file__, 'r') as file:
        script = file.read()

    print("Creating template for remote URL generation.")
    leader = input("Enter the host (host:agent/repository.extension) >")
    extension = input("Enter the extension >")
    key = input("Enter the template name (empty for default) >").strip('\r\n ')
    if key != '':
        print("Note: Access this template by adding '" + key + "' to queries.")
    else:
        key = "default"

    if TEMPLATE_ITEMS is None:
        script = script.replace("TEMPLATE_ITEMS = None", 
        "TEMPLATE_ITEMS = {\n\"" + key + "\" : {\n" +
        "\"leader\" : \"" + leader + "\",\n" +
        "\"extension\" : \"" + extension + "\"\n" +
        "}###ANCHOR FOR REPLACEMENT###\n" +
        "}", 1)
    else:
        script = script.replace("###ANCHOR FOR REPLACEMENT###", 
        ",\n" + "\"" + key + "\" : {\n" +
        "\"leader\" : \"" + leader + "\",\n" +
        "\"extension\" : \"" + extension + "\"\n" +
        "}###ANCHOR FOR REPLACEMENT###", 1)

    with open(__file__, 'w') as file:
        file.write(script)

    if TEMPLATE_ITEMS is None:
        sys.exit(0)

def no_print(*args, **kwargs):
    pass

def print_from(website, agent, repo):
    print("...Creating remote urls for username", agent, "and repo", repo +
            ".")
    print("> git remote add origin git-hub:" + agent + "/" + repo + ".git")

def get_ssh_info(url):
    ssh_url = re.match(r"\w+@\w+\.\w+:(\w+)/([^.]+)\.git", arg)

def print_git(arg, opts):
    log = print if "verbose" in opts else no_print

    # Create a set of git remote urls for this url
    if ssh_url is not None:
        agent = ssh_url.group(1)
        repo = ssh_url.group(2)
        print_from(None, agent, repo)
    http_url = re.match(r"https?://(\w+)\.\w+/(\w+)/([\w\-_]+)(\.git)?", arg)
    if http_url is not None:
        website = http_url.group(1)
        agent = http_url.group(2)
        repo = http_url.group(3)
        print_from(website, agent, repo)

def main(args):
    opts = DEFAULT_PRINTS
    template = "default"
    for a in args:
        if re.match(r"-+r(emote)?", a) is not None and "remote" not in opts:
            opts += "remote"
        elif re.match(r"-+c(lone)?", a) is not None and "clone" not in opts:
            opts += "clone"
        elif re.match(r"-+v(erbose)?", a) is not None and "verbose" not in opts:
            opts += "verbose"
        elif TEMPLATE_ITEMS is not None and a.strip('- ') in TEMPLATE_ITEMS:
            template = a.strip('- ')
        elif re.match(r"-+i(nfo)?", a) is not None and "info" not in opts: 
            opts += "info"
    args = [arg for arg in args if re.match(r"-+", arg) is None] # Simple sanitization
    log = print if "verbose" in opts else no_print

    get_info(opts)
        
    log("Generating URLs for input:\n" + '\n> '.join(args))
    for arg in args:
        print_git(arg, opts)

if __name__ == "__main__":
    main(sys.argv[1:])
