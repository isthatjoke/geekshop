//
// window.onload = function () {
//     let idx, host, src;
//     host = $('.container-services').attr('id');
//     let h60 = $('#h6-0');
//     let img0 = $('#img-0')
//     let img0Atr = $(img0).attr('src')
//     $('.col').on('mouseover', '#img-0', function () {
//         h60.attr('style', 'color:red');
//         src = host + '/static/img/services_branch_red.png';
//         img0.attr('src', src);
//     });
//     $('.col').on('mouseout', '#img-0', function () {
//         h60.attr('style', '');
//         img0.attr('src', img0Atr);
//     });
// }

window.onload = function () {
    let idxImg, idxH6;
    // let src = [];
    //
    // for (let i=0; i<6; i++) {
    //     id = '#img-' + i;
    //     src[i] = $(id).attr('src');
    // }

    $('.picture').on('mouseover', 'img', function () {
        let target = event.target;
        idxImg = target.id.replace('img-', '');
        idxH6 = '#h6-' + idxImg;
        $(idxH6).attr('style', 'color:red');
        target.src = target.src.replace('grey', 'red');
    });

    $('.picture').on('mouseout', 'img', function () {
        let target = event.target;
        idxImg = target.id.replace('img-', '');
        idxH6 = '#h6-' + idxImg;
        $(idxH6).attr('style', '');
        target.src = target.src.replace('red', 'grey');
    });
}