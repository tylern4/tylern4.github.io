---
layout: post
title: The Final Countdown
modified: 2016-01-29
tags: [Code,Linux,OSX]
share: true
---

#Countdown

A lot of times I end up starting a command in one terminal and then want to do something after that command finishes in another window.
I've been using the bash `sleep` command to do this but recently I've wanted to know how long was left in the countdown. So I made a simple
C++ program to do show the time left and added some little things like colors and a progress bar just for fun.

![countdown](/images/countdown.gif)

All the code can be found on my [github] and easily built on both linux and OS X with a simple `make` command.


[github]: http://github.com/tylern4/FinalCountdown

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-72714958-1', 'auto');
  ga('send', 'pageview');

</script>