const ETAPA_ESTRUTURA_START = '0'
const ETAPA_ESTRUTURA_COTACAO = '1'
const ETAPA_ESTRUTURA_FINALIZADA = '3'
const ETAPA_ESTRUTURA_NAO_PODE_LANCE = '4'
const ETAPA_ESTRUTURA_FINALIZADO_SEM_ACORDO = '5'

$.fn.removeClassStartingWith = function (filter) {
    $(this).removeClass(function (index, className) {
        return (className.match(new RegExp("\\S*" + filter + "\\S*", 'g')) || []).join(' ')
    });
    return this;
};
