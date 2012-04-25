<?php

if (function_exists('xhprof_disable')) {
  include_once '/usr/share/pear/xhprof_lib/utils/xhprof_lib.php';
  include_once '/usr/share/pear/xhprof_lib/utils/xhprof_runs.php';
  $xhprof_data = xhprof_disable();
  $xhprof_runs = new XHProfRuns_Default();
  $run_id = $xhprof_runs->save_run($xhprof_data, 'xhprof_testing');

  $data = array('SERVER' => $_SERVER);
  file_put_contents('/var/tmp/perfbucket/' . $run_id . '.json', json_encode($data));
}

