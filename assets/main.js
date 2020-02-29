function setState(name, key, value) {
  state = localStorage.getItem(name);
  if (state === null) {
    state = {};
  } else {
    try {
      state = JSON.parse(state);
    } catch (e) {
      state = {};
    }
  }
  state[key] = value;
  state = JSON.stringify(state);
  localStorage.setItem(name, state);
}

function deleteState(name, key) {
  state = localStorage.getItem(name);
  if (state === null) {
    return;
  }
  try {
    state = JSON.parse(state);
  } catch (e) {
    return;
  }
  delete state[key];
  state = JSON.stringify(state);
  localStorage.setItem(name, state);
}

function getState(name) {
  state = localStorage.getItem(name);
  if (state === null) {
    state = {};
  } else {
    try {
      state = JSON.parse(state);
    } catch (e) {
      state = {};
    }
  }
  return state;
}

function verticalDividerMouseDown(evt) {
  evt.preventDefault();
  $(window).mousemove(verticalDividerMouseMove).mouseup(verticalDividerMouseUp);
  $('aside').data('initial-width', $('aside').width()).data('initial-pageX', evt.pageX);
}

function verticalDividerMouseMove(evt) {
  evt.preventDefault();
  $('aside').width(evt.pageX - $('aside').data('initial-pageX') + $('aside').data('initial-width'));
}

function verticalDividerMouseUp(evt) {
  evt.preventDefault();
  $(window).off('mousemove', verticalDividerMouseMove).off('mouseup', verticalDividerMouseUp);
  setState('aside', 'width', $('aside').width());
}

$(function() {
  $('.file-tree li').has('.dir').click(function(evt) {
    link = $(this).children('.dir').children('a');
    isme = (evt.target == this) || $(evt.target).is(link);
    if (isme && $(this).hasClass('expand')) {
      evt.preventDefault();
      $(this).removeClass('expand').addClass('collapse');
      setState('expand', $(this).attr('id'), 1);
    } else if (isme && $(this).hasClass('collapse')) {
      evt.preventDefault();
      $(this).removeClass('collapse').addClass('expand');
      deleteState('expand', $(this).attr('id'));
    }
  });

  for (let id of Object.keys(getState('expand'))) {
    $('#' + id).removeClass('expand').addClass('collapse');
  }

  let names_to_nodes = {};

  $('.n, .na, .nb, .bp, .nc, .no, .nd, .ni, .ne, .nf, .fm, .py, .nl, .nn, .nx, .nt, .nv, .vc, .vg, .vi, .vm').each(function() {
    name = this.innerText;
    url = encodeURI("/search?q=" + name);
    $(this).wrapInner('<a class="hh" href="' + url + '"></a>');
    if (name in names_to_nodes) {
      names_to_nodes[name].push(this);
    } else {
      names_to_nodes[name] = [this];
    }
  });

  $('.hh').hover(function() {
    $('.highlight').removeClass('highlight');
    name = this.innerText;
    if (name in names_to_nodes) {
      $(names_to_nodes[name]).addClass('highlight');
    }
  });

  $('.file-tree').scroll(function() {
    id = $(this).attr('id');
    st = $(this).scrollTop();
    setState('scroll-top', id, st);
  });

  for (let [id, st] of Object.entries(getState('scroll-top'))) {
    $('#' + id).scrollTop(st);
  }

  $('.vertical.divider').mousedown(verticalDividerMouseDown);

  let asideState = getState('aside');
  if (asideState.hasOwnProperty('width')) {
    //$('aside').width(asideState.width);
  }
});
