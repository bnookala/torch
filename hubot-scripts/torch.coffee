# control script for Torch control of browsers at remote displays
#
# list screens - list available screens for a control group # show screens - show overlays with aliases on screens for a control group
# list tabs on <screen> - list tab URLs on a screen
# show (<tab index>|<alias>|<url>) on <screen> (as <alias>) - change screen to given tab index or alias
# rotate <screen> every <time> - automatically advance through tabs every <time> interval
# close tab on <screen> - close current tab
# refresh <screen> - refreshes current tab on screen
# next <screen> - changes to next tab on screen
# prev(ious) <screen> - changes to previous tab on screen

qs = require 'querystring'

TORCH_ADDRESS = 'localhost:9001'

tellTorch = (msg, command, screen, extra) ->
  data = qs.stringify extra
  msg.http('http://#{TORCH_ADDRESS}')
    .path('/#{screen}/#{command}?#{data}')
    .header('X-Username', msg.message.user.name)
    .header('X-Channel', msg.message.user.room)
    .get() (err, res, body) ->
      if res.statusCode == 200
        msg.send body
      else
        msg.send err

module.exports = (robot) ->
  robot.respond /list screens$/i, (msg) ->
    tellTorch msg, 'list', undefined, {}
  robot.respond /show screens$/i, (msg) ->
    tellTorch msg, 'enumerate', undefined, {}
  robot.respond /list tabs on (\w+)$/i, (msg) ->
    tellTorch msg, 'list', msg.match[1], {}
  robot.respond /what's on (\w+)$/i, (msg) ->
    tellTorch msg, 'details', msg.match[1], {}
  robot.respond /show (\S+) on (\w+)$/i, (msg) ->
    tellTorch msg, 'show', msg.match[2], {'cmd': msg.match[1]}
  robot.respond /close tab on (\w+$)/i, (msg) ->
    tellTorch msg, 'close', msg.match[1], {}
  robot.respond /refresh (\w+$)/i, (msg) ->
    tellTorch msg, 'refresh', msg.match[1], {}
  robot.respond /next (\w+$)/i, (msg) ->
    tellTorch msg, 'next', msg.match[1], {}
  robot.respond /prev(ious)? (\w+$)/i, (msg) ->
    tellTorch msg, 'prev', msg.match[1], {}
