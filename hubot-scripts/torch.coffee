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

TORCH_ADDRESS = '10.10.1.107'

tellTorch = (msg, path, extra={}) ->
  data = qs.stringify extra
  path = path + '?' + data

  msg.http('http://' + TORCH_ADDRESS)
    .path(path)
    .port('5000')
    .header('X-User', msg.message.user.name)
    .header('X-Channel', msg.message.user.room)
    .get() (err, res, body) ->
      if res.statusCode == 200
        msg.send body
      else
        msg.send "some shit is fucked up"

module.exports = (robot) ->
  robot.respond /list screens$/i, (msg) ->
    tellTorch msg, 'list'

  robot.respond /show screens$/i, (msg) ->
    tellTorch msg, 'enumerate'

  robot.respond /list tabs on (\w+)$/i, (msg) ->
    tellTorch msg, "#{msg.match[1]}/list"

  robot.respond /what's on (\w+)$/i, (msg) ->
    tellTorch msg, "#{msg.match[1]}/details"

  robot.respond /show (\S+) on (\w+)$/i, (msg) ->
    tellTorch msg, "#{msg.match[2]}/show", {'cmd': msg.match[1]}

  robot.respond /close tab on (\w+$)/i, (msg) ->
    tellTorch msg, "#{msg.match[1]}/close"

  robot.respond /refresh (\w+$)/i, (msg) ->
    tellTorch msg, "#{msg.match[1]}/refresh"

  robot.respond /show next (\w+$)/i, (msg) ->
    tellTorch msg, "#{msg.match[1]}/next"

  robot.respond /show prev(ious)? (\w+$)/i, (msg) ->
    tellTorch msg, "#{msg.match[1]}/previous"
