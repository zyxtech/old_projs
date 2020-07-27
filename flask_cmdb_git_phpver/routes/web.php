<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
Route::get('now', function () {
    return date("Y-m-d H:i:s");
});

// app/Http/routes.php
Route::get('test/form', [
    'uses' => 'TestController@create',
    'as' => 'test.form'
]);

Route::post('test/store', [
    'uses' => 'TestController@store',
    'as' => 'test.store'
]);

Route::get('test', [
    'uses' => 'TestController@listResult',
    'as' => 'test.listResult'
]);

Route::get('test/listData', [
    'uses' => 'TestController@listData',
    'as' => 'test.listData'
]);

Route::get('test/form_del', [
    'uses' => 'TestController@del',
    'as' => 'test.del'
]);