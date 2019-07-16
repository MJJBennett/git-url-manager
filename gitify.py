#!/usr/bin/env python3
import sys, re

DEFAULT_PRINTS = [
    "remote"
]

TEMPLATE_ITEMS = None
template = None

def get_info(opts):
    if TEMPLATE_ITEMS is not None and "info" not in opts:
        return

    with open(__file__, 'r') as file:
        script = file.read()

    print("Creating template for remote URL generation.")
    leader = input("Enter the host (host:agent/repository.extension) > ")
    extension = input("Enter the extension > ")
    key = input("Enter the template name (empty for default) > ").strip('\r\n ')
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

def get_id(website, agent, repo):
    t = TEMPLATE_ITEMS[template] if template in TEMPLATE_ITEMS else TEMPLATE_ITEMS["default"]
    return t["leader"] + ":" + agent + "/" + repo + '.' + t["extension"]

def print_remote(website, agent, repo):
    print("> git remote add origin", get_id(website, agent, repo))

def print_clone(website, agent, repo):
    print("> git clone", get_id(website, agent, repo))

def print_clean(website, agent, repo):
    print(get_id(website, agent, repo))

def get_ssh_info(url):
    ssh_url = re.match(r"\w+@\w+\.\w+:(\w+)/([^.]+)\.git", url)
    if ssh_url is not None:
        return (ssh_url.group(1), ssh_url.group(2))
    return None

def get_http_info(url):
    http_url = re.match(r"https?://(\w+)\.\w+/(\w+)/([\w\-_]+)(\.git)?", url)
    if http_url is not None:
        return (http_url.group(1), http_url.group(2), http_url.group(3))
    return None

def print_git(arg, opts):
    log = print if "verbose" in opts else no_print

    # Create a set of git remote urls for this url
    if get_ssh_info(arg) is not None:
        agent, repo = get_ssh_info(arg)
        website = None
    elif get_http_info(arg) is not None:
        website, agent, repo = get_http_info(arg)
    else:
        log("Could not find URL information in argument:", arg)
        return

    if "plumb" in opts:
        log("Printing clean information.")
        print_clean(website, agent, repo)
        return
    if "remote" in opts:
        log("Printing remote information.")
        print_remote(website, agent, repo)
    if "clone" in opts:
        log("Printing clone information.")
        print_clone(website, agent, repo)

def main(args):
    opts = DEFAULT_PRINTS
    global template
    template = "default"
    for a in args:
        if re.match(r"-+r(emote)?", a) is not None and "remote" not in opts:
            opts.append("remote")
        elif re.match(r"-+c(lone)?", a) is not None and "clone" not in opts:
            opts.append("clone")
        elif re.match(r"-+v(erbose)?", a) is not None and "verbose" not in opts:
            opts.append("verbose")
        elif TEMPLATE_ITEMS is not None and a.strip('- ') in TEMPLATE_ITEMS:
            template = a.strip('- ')
        elif re.match(r"-+i(nfo)?", a) is not None and "info" not in opts: 
            opts.append("info")
        # "clean" overrides and only prints the actual URL output, nothing else
        # for use in other scripts/aliases
        elif re.match(r"-+p(lumb)?", a) is not None and "plumb" not in opts:
            opts.append("plumb")
    args = [arg for arg in args if re.match(r"-+", arg) is None] # Simple sanitization
    # This doesn't remove 'key' arguments if given without a preceding dash
    # So we just need to remember that args might not be fully sanitized

    log = print if "verbose" in opts else no_print

    get_info(opts)
        
    log("Generating URLs for input:\n" + '\n> '.join(args))
    for arg in args:
        print_git(arg, opts)

if __name__ == "__main__":
    main(sys.argv[1:])
