const ETAPA_ESTRUTURA_START = '0'
const ETAPA_ESTRUTURA_FORNECEDOR = '1'
const ETAPA_ESTRUTURA_ADMINISTRADOR = '2'
const ETAPA_ESTRUTURA_FINALIZADA = '3'
const ETAPA_ESTRUTURA_NAO_PODE_LANCE = '4'
const ETAPA_ESTRUTURA_FINALIZADO_SEM_ACORDO = '5'


function upStatusCelula(celula, status, bg){
    span_status = celula.find('span:eq(0)')
    span_status.text(status);
    span_status.removeClassStartingWith('text-bg');
    span_status.addClass('text-bg-'+bg);
}

$.fn.removeClassStartingWith = function (filter) {
    $(this).removeClass(function (index, className) {
        return (className.match(new RegExp("\\S*" + filter + "\\S*", 'g')) || []).join(' ')
    });
    return this;
};

angular.module('app', [])
    .directive('angCelPreco', function(){
        return function (scope, elem, attr){

            span_status = elem.find('span:eq(0)')
            switch (elem.attr('status')) {
                case ETAPA_ESTRUTURA_FINALIZADA:
                    upStatusCelula(elem, 'ACORDO', 'success');
                    break;
                case ETAPA_ESTRUTURA_ADMINISTRADOR:
                    upStatusCelula(elem, 'PROPOSTA', 'warning');
                    elem.attr('data-bs-target', '#formulario-contra');
                    elem.attr('data-bs-toggle', 'modal');
                    elem.addClass('celula-preco');
                    elem.append(`<input type="text" name="${elem.attr('id')}">`)
                    break;
                case ETAPA_ESTRUTURA_FORNECEDOR:
                    upStatusCelula(elem, 'C.PROPOSTA', 'info');
                    break;
                case ETAPA_ESTRUTURA_NAO_PODE_LANCE:
                    upStatusCelula(elem, 'C.PROPOSTA', 'info');
                    break;
                case ETAPA_ESTRUTURA_FINALIZADO_SEM_ACORDO:
                    upStatusCelula(elem, 'S/ACORDO', 'light');
                    break;
                case ETAPA_ESTRUTURA_START:
                    upStatusCelula(elem, 'START', 'light');
                    break;
            }


        }
    })

    .directive('angWindownewcusto', function(){
        return function(scope, elem, attr){
            scope.maislance = true
            scope.novopreco = 0
            scope.decisao = 'recusado'
            var cel;

            elem.on('show.bs.modal', function(event){
                const item = event.relatedTarget
                estrutura = item.id
                cel = $(item)
                $('#proposta-fornecedor').text(item.getAttribute('proposta-fornecedor'))
            })

            elem.find('#btn-save-form').on('click', function(){
                if (scope.decisao == 'aceito'){
                    cel.find("input").val('ACEITO')
                    upStatusCelula(cel, '****ACORDO', 'success')
                }else if(scope.decisao == 'recusado'){
                    upStatusCelula(cel, '*C.PROPOSTA*', 'info')
                    cel.find('#preco-raw').text(scope.novopreco.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'}))
                    cel.find("input").val(`RECUSADO:${scope.novopreco}:${scope.maislance}`)

                }
            })
        }
    })