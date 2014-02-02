<!doctype html>
<html lang="en">
<head>
    <meta charset='utf-8'>
    <title>Webfs</title>
    <link rel="stylesheet" href="/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-default" role="navigation">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navcol">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/">Wombat <small><span class="glyphicon glyphicon-cloud"></span></small></a>
            </div>
            <div class="collapse navbar-collapse" id="navcol">

                <ul class="nav navbar-nav">
                </ul>

            </div>
        </div>
    </nav>

    <div class="container">
        <div class="row">
            <div class="col-lg-6 col-lg-offset-3 col-md-8 col-md-offset-2">
            <ul class="nav nav-tabs nav-justified">
                <li class="active"><a href="#login" data-toggle="tab">Log in</a></li>
                <li><a href="#reg" data-toggle="tab">Register</a></li>
            </ul>
            <div class="tab-content">
                <div class="tab-pane active" id="login">
                    <h3>Login</h3>
                    <form action="login" method="post" name="login" role="form">
                        <div class="form-group">
                            <input class="form-control" type="text" name="username" placeholder="username">
                        </div>
                        <div class="form-group">
                            <input class="form-control" type="password" name="password" placeholder="password">
                        </div>

                        <button type="submit" class="btn btn-primary">Log in</button>
                    </form>
                </div>
                <div class="tab-pane" id="reg">
                    <h3>Sign up</h3>
                    <form action="register" method="post" name="signup" role="form">
                        <div class="form-group">
                            <input class="form-control" type="text" name="username" placeholder="username">
                        </div>
                        <div class="form-group">
                            <input class="form-control" type="password" name="password" placeholder="password">
                        </div>
                        <div class="form-group">
                            <input class="form-control" type="email" name="email_address" placeholder="Email">
                        </div>

                        <button type="submit" class="btn btn-primary">Register</button>
                    </form>
                    <br />
                </div>
            </div>
        </div>
    </div>
    <script src="/js/libs/jquery-2.1.0.min.js"></script>
    <script src="/js/bootstrap.min.js"></script>
</body>
</html>
