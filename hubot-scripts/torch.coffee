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

TORCH_ADDRESS = '127.0.0.1:9001'

tellTorch = (msg, path, extra={}) ->
  data = qs.stringify extra

  msg.http('http://#{TORCH_ADDRESS}/#{path}?#{data}')
    .header('X-User', msg.message.user.name)
    .header('X-Channel', msg.message.user.room)
    .get() (err, res, body) ->
      if res.statusCode == 200
        body = JSON.parse body
        if body.success? and not body.success
          msg.send body.msg
          return
        msg.send body
      else
        msg.send err

module.exports = (robot) ->
  robot.respond /list screens$/i, (msg) ->
    tellTorch msg, 'list'

  robot.respond /show screens$/i, (msg) ->
    tellTorch msg, 'enumerate'

  robot.respond /list tabs on (\w+)$/i, (msg) ->
    tellTorch msg, '#{msg.match[1]}/list'

  robot.respond /what's on (\w+)$/i, (msg) ->
    tellTorch msg, '#{msg.match[1]}/details'

  robot.respond /show (\S+) on (\w+)$/i, (msg) ->
    tellTorch msg, '#{msg.match[2]}/show', {'cmd': msg.match[1]}

  robot.respond /close tab on (\w+$)/i, (msg) ->
    tellTorch msg, '#{msg.match[1]}/close'

  robot.respond /refresh (\w+$)/i, (msg) ->
    tellTorch msg, '#{msg.match[1]}/refresh'

  robot.respond /next (\w+$)/i, (msg) ->
    tellTorch msg, '#{msg.match[1]}/next'

  robot.respond /prev(ious)? (\w+$)/i, (msg) ->
    tellTorch msg, '#{msg.match[1]}/previous'
