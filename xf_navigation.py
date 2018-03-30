


class XFNavigationLink:
    def __init__(self, caption=None, url=None):
        self.caption = caption
        self.url = url
        self.sub_navigation_links = []


class XFNavigationSection:
    def __init__(self, name=None, icon=None):
        self.name = name
        self.icon = icon
        self.navigation_links = []

    def add_navigation_link(self, navigaton_link):
        self.navigation_links.append(navigaton_link)



class XFNavigationHeader:

    def __init__(self, name=None):
        self.name = name
        self.navigation_sections = []

    def add_subsection(self, sub_section):
        self.navigation_sections.append(sub_section)


def add_navigation(navigation_tree, header_name="Home", section_name="Welcome", url=None, icon=None, caption=None, parent_caption=None):
    # !Recursive

    # Search for a header with the given header_name in the navigation_tree
    for header in navigation_tree:
        if header.name == header_name:
            # Header found, now search for a section
            for section in header.navigation_sections:
                if section.name == section_name:
                    # Section found, add the link to it
                    if parent_caption == None:
                        section.navigation_links.append(XFNavigationLink(caption=caption, url=url))
                        return
                    else:
                        # Search for a parent caption link
                        print("adding %s to %s with url %s" % (caption, parent_caption, url))
                        for navigation_link in section.navigation_links:
   #                         print ">>> searching for " % (navigation_link.caption, parent_caption, url)
                            if navigation_link.caption == parent_caption:
                               navigation_link.sub_navigation_links.append(XFNavigationLink(caption=caption, url=url))

                        return

            # Section not found, create and add it
            header.navigation_sections.append(XFNavigationSection(name=section_name, icon=icon))

            # Repeat the procedure, and this time the section is there so it will be found
            add_navigation(navigation_tree, header_name, section_name, url, icon, caption, parent_caption)
            return

    # Header not found, so create it and add it
    navigation_tree.append(XFNavigationHeader(name=header_name))

    # Repeat the procedure and this time it will be found
    add_navigation(navigation_tree, header_name, section_name, url, icon, caption, parent_caption)


