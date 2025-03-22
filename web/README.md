# Building static assets

Use [Webpack](https://webpack.js.org/) to bundle, compile and minify CSS, JS, fonts and images.

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

Components should only be included if they are used in the service, in order to keep distributon file sizes small. The `/web/src/scss/main.scss` and `/web/src/js/main.mjs` files only imports the components that are used.

### Format source code

Use [Prettier](https://prettier.io/), an opinionated code formatter, for consistency:

```shell
npm run format
```

### Build assets

Output compiled CSS, JS, fonts and images to `./dist`:

```shell
npm run build
```

### Watch changes

Rebuild distribution assets automatically when source is changed:

```shell
npm run watch
```

### Update dependencies

To update Node package dependencies (such as [bootstrap](https://www.npmjs.com/package/bootstrap)), use [npm-check-updates](https://www.npmjs.com/package/npm-check-updates):

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
