import gsaio.shellsignal02


def test_alert(loop):
    collected_msgs = []
    loop.create_task(shellsignal02.alert(lambda msg: collected_msgs.append(msg)))
    loop.call_later(1, loop.stop)
    loop.run_forever()
    assert collected_msgs[0] == 'Alert!'