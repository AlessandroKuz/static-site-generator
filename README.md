# static-site-generator

The following is a project that enables the user to convert Markdown documents into a html website.

For a demo check the `deploy` branch [here](https://github.com/AlessandroKuz/static-site-generator/tree/deploy), or
visit directly the [generated website](http://alessandrokuz.info/static-site-generator/), made from the following
[Markdown documents](https://github.com/AlessandroKuz/static-site-generator/tree/deploy/content).

The project is developed in `Python` following the
[related boot.dev course](https://www.boot.dev/courses/build-static-site-generator-python).

## Table of Contents

1. [Execution](#execution)
2. [Tests](#tests)
3. [Build](#build)
4. [How to Use](#how-to-use)
5. [Future Roadmap](#future-roadmap)

## Execution

To run the program execute `./main.sh`.

## Tests

To run the tests make sure you have python installed, then, on Linux and MacOS, run `./test.sh`.

## Build

On the deployment branch you can also execute `./build.sh` to build the HTML files, using the repo URL.

## How to Use

1. Git clone the repo with the following command:

    ```shell
    git clone https://github.com/AlessandroKuz/static-site-generator.git
    ```

2. Go inside the cloned repository

    ```shell
    cd static-site-generator
    ```

3. Copy your markdown files into `content`
4. Run the program
    - On windows:
    ```powershell
    python src\main.py
    cd public  # or "cd docs" if on deploy branch
    python3 -m http.server 8888
    ```
    - On Linux, MacOS & WSL
    ```shell
    ./main.sh
    ```
5. Your out will be in `public/` if your on the `main` branch or in `docs/` if you're on the `deplay` branch.

That's it! You can customize the look of the website by changing `template.html` and the files inside of `static/`.

## Markdown reference

- [Simple Markdown Guide](https://www.markdownguide.org/cheat-sheet/)
- [Basic Syntax and best practices](https://www.markdownguide.org/basic-syntax/)
- [Markdown book](https://www.markdownguide.org/book/)

## Future Roadmap

- [ ] Add support for self-closing tags (i.e., `img`, `hr`)
    - Rework `img`

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

- [ ] Add support for nested elements
    - [ ] nested inline elements
    - [ ] nested block elements
        - for example blockquote within blockquote

[//]: # (- [ ] Add support for tabbed text to become a quote?)

[//]: # (- [ ] Switch from `<b>` and `<i>` tags to `<strong>` and `<em>`?)

- [ ] Add support for nested "LeafNodes" (i.e., an `italic` tag withing a `bold` one or viceversa) -
    - recursive?
    - 1/2 level(s) deep?

- [ ] Fix: the delimiters order inside ALLOWED_INLINE_DELIMITERS matters to the way that inline elements are split into
  nodes and their type.
    - This needs a rework, especially in the future to allow nested blocks no matter the order

- [ ] Update the docs to specify in detail what types are supported, which are currently not supported and so on

- [ ] Add a mkdocs section for reference

- [ ] Add support for Text splits for other types than TextType.TEXT.

- [ ] Use pydantic for class definition

- [ ] Add a mkdocs section for reference

- [ ] Instead of reading it each time, load the contents of the template just once, and pass it as an argument

- [ ] Simplify the usage of the program to make the convertion easier
