# static-site-generator

The following is a project that enables the user to convert Markdown documents into a html website.

The project is developed in python following
the [related boot.dev course](https://www.boot.dev/courses/build-static-site-generator-python).

## Future Roadmap

- [ ] add support for self-closing tags (i.e., `img`, `hr`)

[//]: # (    <area> - Specifies clickable areas in image maps)

[//]: # (    <base> - Sets base URL for relative links)

[//]: # (    <br> - Creates a line break)

[//]: # (    <col> - Defines column properties in tables)

[//]: # (    <embed> - Embeds external content &#40;like plugins&#41;)

[//]: # (    <hr> - Creates a horizontal rule)

[//]: # (    <img> - Embeds images)

[//]: # (    <input> - Creates form input fields)

[//]: # (    <link> - Links external resources &#40;stylesheets, etc.&#41;)

[//]: # (    <meta> - Provides document metadata)

[//]: # (    <param> - Defines parameters for objects)

[//]: # (    <source> - Specifies media sources)

[//]: # (    <track> - Defines text tracks for media)

[//]: # (    <wbr> - Suggests potential line break points)

- [ ] add support for nested "LeafNodes" (i.e., an `italic` tag tag withing a `bold` one or viceversa) -
    - recursive?
    - 1/2 level(s) deep?

- [ ] Fix: the delimiters order inside of ALLOWED_DELIMITERS matters to the way that inline elements are split into nodes and their type.
    - This needs a rework, especially in the future to allow nested blocks no matter the order

- [ ] Update the docs to specify in detail what types are supported, which are currently not supported and so on

- [ ] Add a mkdocs section for reference
