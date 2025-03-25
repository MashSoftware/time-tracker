# Building static assets

Use [Webpack](https://webpack.js.org/) to bundle, compile and minify JavaScript, SCSS, images, and fonts, while optimising the output for performance. It uses various loaders and plugins to process files and generate the final build:

- [**CSS Minimizer Webpack Plugin**](https://webpack.js.org/plugins/css-minimizer-webpack-plugin/): Uses [CSSNANO](https://cssnano.github.io/cssnano/) to minimise the CSS output, reducing file size and improving page load times.
- [**PostCSS Preset Env**](https://github.com/csstools/postcss-plugins/tree/main/plugin-packs/postcss-preset-env): Uses [Autoprefixer](https://github.com/postcss/autoprefixer) to add vendor prefixes and ensure compatibility with older browsers.
- [**Babel Preset Env**](https://babeljs.io/docs/babel-preset-env): Transpiles ES6+ JavaScript for cross-browser compatibility while allowing the use of modern JavaScript features.
- [**Webpack Dev Server**](https://webpack.js.org/configuration/dev-server/): Serves files from the output directory with live reloading for development workflows.

## Prerequisites

- [Node Version Manager (nvm)](https://github.com/nvm-sh/nvm)

## Get started

1. Install the correct version of [Node.js](https://nodejs.org/en). This is determined by the `.nvmrc` file and is typically the latest LTS release codename.

   ```shell
   nvm install
   ```

2. Install the Node package dependencies from [npm](https://www.npmjs.com/):

   ```shell
   npm install
   ```

## How to

### Use Bootstrap components

The `main.scss` file at `/src/scss` is highly selective about which `components` are imported in order to keep distributon file sizes small. Simply uncomment any other components in `main.scss` that you need to use.

The same approach applies to JS; the `main.mjs` file at `/src/js` only imports JS for the components being used.

### Format source code

Use [Prettier](https://prettier.io/), an opinionated code formatter, for consistency.

To check formatting (without changing):

```shell
npm run format:check
```

To reformat files:

```shell
npm run format:fix
```

### Lint source code

Use [ESLint](https://eslint.org/) to statically analyse your code to quickly find problems.

To check for issues:

```shell
npm run lint:check
```

To attempt to automatically fix issues:

```shell
npm run lint:fix
```

### Build assets

Use [Webpack](https://webpack.js.org/) loaders and plugins to output CSS, JS, fonts and images to `./dist`:

```shell
npm run build
```

### Watch changes

Rebuild distribution assets automatically when source is changed:

```shell
npm run watch
```

### Update dependencies

Use [npm-check-updates](https://www.npmjs.com/package/npm-check-updates) to update Node package dependencies (such as [bootstrap](https://www.npmjs.com/package/bootstrap)):

```shell
ncu -u
```

If you want to be more cautious you can check only for patch or minor level updates:

```shell
ncu --target patch -u
```

```shell
ncu --target minor -u
```
