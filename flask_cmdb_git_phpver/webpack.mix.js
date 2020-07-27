let mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

mix.js('resources/assets/js/app.js', 'public/js')
   .sass('resources/assets/sass/app.scss', 'public/css');
 mix.js('resources/assets/js/jquery-3.3.1.min.js', 'public/js')
 mix.copy('resources/assets/package/bootstrap_local','public/package/bootstrap_local');
 mix.copy('resources/assets/package/metisMenu','public/package/metisMenu');
 mix.copy('resources/assets/package/raphael','public/package/raphael');
 mix.copy('resources/assets/package/theme','public/package/metisMenu');
 
 mix.copy('resources/assets/sass/font-awesome', 'public/css/font-awesome');
 
 mix.autoload({
    jQuery: 'jquery',
    $: 'jquery',
    jquery: 'jquery'
});
