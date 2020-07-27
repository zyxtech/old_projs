<?php

namespace App\Forms;

use Kris\LaravelFormBuilder\Form;

class TestForm extends Form
{
    public function buildForm()
    {
        $this
            ->add('name', 'text', [
                'rules' => 'required|min:5'
            ])
            ->add('lyrics', 'textarea')
            ->add('publish', 'checkbox');
    }
}
