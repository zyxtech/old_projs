<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controller as BaseController;
use Kris\LaravelFormBuilder\FormBuilder;
use App\Forms\TestForm;
use Illuminate\Http\Request;
use App\Http\Requests;

class TestController extends BaseController {

    public function create(FormBuilder $formBuilder)
    {
        $form = $formBuilder->createByArray([
                        [
                            'name' => 'name',
                            'type' => 'text',
                        ],
                        [
                            'name' => 'lyrics',
                            'type' => 'textarea',
                        ], 
                        [
                            'name' => 'publish',
                            'type' => 'checkbox'
                        ],
                    ]
            ,[
            'method' => 'POST',
            'url' => route('test.store')
        ]);
        $form
            ->add('submit', 'submit', ['label' => 'Save form'])
            ->add('clear', 'reset', ['label' => 'Clear form']);
        return view('test.create', compact('form'));
    }
    
    public function store(FormBuilder $formBuilder)
    {
        $form = $formBuilder->create(TestForm::class);

        if (!$form->isValid()) {
            return redirect()->back()->withErrors($form->getErrors())->withInput();
        }
        
    
       \App\Test::create([
            'name'   => $form->getField("name")->getRawValue(),
            'lyrics'    =>$form->getField("lyrics")->getRawValue(),
            'publish' => $form->getField("publish")->getRawValue(),
        ]);
        
       return redirect('test');
    }
    
    public function listResult()
    {
         $listnames = ["id", "name", "lyrics", "publish", "ops"];
         return view('test.listresult',['listnames' => $listnames,'formurl'=>"/test/form", 'name' => "testList", 'ajaxl' => "/test/listData"]);
         
    }
    public function listData()
    {
        $dataResult = [];
         foreach (\App\Test::all() as $test){
             $dataele = [];
              array_push($dataele,$test->id) ;
             array_push($dataele,$test->name) ;
              array_push($dataele,$test->lyrics) ;
               array_push($dataele,$test->publish) ;
             array_push($dataResult,$dataele);
         }
         return response()->json(["data"=>$dataResult],200) ;
         
    }
    
    public function del(Request $request)
    {
         $result = \App\Test::destroy($request->id);
         if ($result == 1){
             return response()->json(["data"=>"success"],200) ;
         }
         else{
             return response()->json(["data"=>"failed"],200) ;
         }
    }
}

