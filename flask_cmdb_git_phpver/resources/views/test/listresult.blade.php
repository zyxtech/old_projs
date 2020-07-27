


<!-- resources/views/test/create.blade.php -->
@extends('home')

@section('css')
   <link href="{{{  asset('package/DataTables/DataTables-1.10.16/css/dataTables.bootstrap.css') }}}" rel="stylesheet">
   <link href="{{{  asset('package/DataTables/Responsive-2.2.1/css/responsive.bootstrap.css') }}}" rel="stylesheet">
   
@endsection

@section('content')
    
    <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">
                    @if ( $name != NULL)
                    {{$name}}
                    @endif
                    </h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row" style="width:100%">
                <table id="example" class="table table-striped "  cellspacing="0" width="100%">
                    <thead>
                        <tr>
                            @foreach ($listnames as $listname)
                                <th> {{ $listname }}</th>
                            @endforeach
                        </tr>
                    </thead>
                    <tfoot>
                        <tr>
                             @foreach ($listnames as $listname)
                                <th> {{ $listname }}</th>
                            @endforeach
                        </tr>
                    </tfoot>
                </table>

                <!-- /.col-lg-12 -->
            </div>
@endsection

@section('js')
<script src="{{ asset('package/DataTables/DataTables-1.10.16/js/jquery.dataTables.min.js') }}"></script>
<script src="{{ asset('package/DataTables/DataTables-1.10.16/js/dataTables.bootstrap.min.js') }}"></script>
<script src="{{ asset('package/DataTables/Responsive-2.2.1/js/dataTables.responsive.js') }}"></script>
<script src="{{ asset('package/DataTables/Buttons-1.5.0/js/dataTables.buttons.min.js') }}"></script>
<script src="{{ asset('package/DataTables/JSZip-2.5.0/jszip.min.js') }}"></script>
<script src="{{ asset('package/DataTables/pdfmake-0.1.32/pdfmake.min.js') }}"></script>
<script src="{{ asset('package/DataTables/pdfmake-0.1.32/vfs_fonts.js') }}"></script>
<script src="{{ asset('package/DataTables/Buttons-1.5.0/js/buttons.html5.js') }}"></script>
<script>
    var table;
    $(document).ready(function() {
            table = $('#example').DataTable({
                "ajax": "@if ( $name != NULL) {{$ajaxl}}@endif",
                "columnDefs": [{
                    "targets": -1,
                    "mData": null,
                    "mRender": function (data, type, full) {
                        return '<a class="btn btn-info btn-sm" href={{ $formurl }}?id=' + full[0] + '>' + 'edit' + '</a>' +
                            '<a href="javascript:void(0)" class="btn btn-danger btn-sm delbuttons" >' + 'del' + '</a>';
                    }
                },{ "visible": false, "targets": 0 }],
                dom: 'Bfrtip',
                buttons: [
                    {
                        text: 'add',
                        action: function ( e, dt, node, config ) {
                            window.location.href = '{{ $formurl }}'
                        }
                    },
                    'copyHtml5',
                    'excelHtml5',
                    {
                        extend: 'csvHtml5',
                        charset: 'utf-8',
                        sCharSet: 'utf8',
                        aButtons: true
                    }
                ],
                responsive: true
            });
            function hidetr(){
                table.row('.selected').remove().draw( false );
            }
            $('#example tbody').on( 'click', '.delbuttons', function (event) {
                var data = table.row( $(this).parents('tr') ).data();
                $(this).parents('tr').addClass('selected');
                var thistr = $(this).parents('tr');
                $.ajax({url: "{{ $formurl }}_del?id="+data[0], success: function(result){

                    if(result.data == "success"){
                        hidetr()
                    }
                    else{
                        if (result.info != null)
                            alert(result.info)
                        else
                            alert("failed，try again！");
                        $(thistr).removeClass('selected');

                    }
                }});
                 event.stopPropagation();
            } );



    });
    </script>
@endsection
