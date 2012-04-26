<html>
  <head>
    <meta http-equiv="refresh" content="60">
    <title>Report Generated <?php echo date('c'); ?></title>
  </head>
  <body>
    <pre>
<?php htmlentities(passthru('/usr/bin/perfbucket show pages')); ?>
    </pre>
  </body>
</html>
