# 홈 화면 앱으로 설치 버튼을 보여줄 '매일 쓰는 도구' (경로, 앱 이름(홈 화면 글자), 아이콘 이모지, 아이콘 배경색)
APPS = [
    ('/medical/pharmacy-open.html', '문 연 약국', '💊', '#FFF1F3'),
    ('/medical/emergency-room.html', '응급실', '🚑', '#FFF1F3'),
    ('/life/air-quality.html', '미세먼지', '😷', '#EEF4FF'),
    ('/drive/gas-station.html', '싼 주유소', '⛽', '#FFF4E6'),
    ('/drive/ev-charger.html', '충전소', '🔌', '#EEF4FF'),
    ('/drive/parking.html', '주차장', '🅿️', '#EEF4FF'),
    ('/drive/rest-area.html', '휴게소', '🛣️', '#FFF4E6'),
    ('/life/toilet.html', '화장실', '🚻', '#EEF4FF'),
    ('/trip/festival.html', '축제 지도', '🎉', '#FFF4E6'),
    ('/trip/camping.html', '캠핑장', '🏕️', '#FFF4E6'),
    ('/life/route-navi.html', '노선 내비', '🚌', '#EEF4FF'),
    ('/life/taxi-fare.html', '택시비', '🚕', '#FFF9DB'),
    ('/life/midpoint.html', '중간지점', '📍', '#FFF1F3'),
    ('/life/split-bill.html', 'N빵', '🧾', '#F3F0FF'),
    ('/life/subsidy.html', '지원금', '💰', '#FFF9DB'),
    ('/ipsi/gichul/', '수능 기출', '📚', '#EEF4FF'),
    ('/calendar/exam-schedule.html', '시험일정', '🗓️', '#F3F0FF'),
    ('/calendar/exam-dday.html', '시험 D-day', '🎯', '#FFF1F3'),
    ('/calendar/dday.html', 'D-day', '📅', '#EEF4FF'),
    ('/calendar/timer.html', '타이머', '⏲️', '#F3F0FF'),
    ('/calendar/pomodoro.html', '뽀모도로', '🍅', '#FFF1F3'),
    ('/calendar/alarm-clock.html', '알람', '⏰', '#FFF4E6'),
    ('/calendar/big-clock.html', '큰 시계', '🕰️', '#F3F0FF'),
    ('/calendar/holidays.html', '공휴일', '🏖️', '#EEF4FF'),
    ('/calendar/lunar.html', '음력 변환', '🌙', '#F3F0FF'),
    ('/text/lotto.html', '로또 번호', '🎱', '#FFF9DB'),
    ('/text/char-count.html', '글자 수', '🔤', '#EEF4FF'),
    ('/text/random-pick.html', '추첨', '🎲', '#F3F0FF'),
    ('/life/tally-counter.html', '카운터', '🔢', '#EEF4FF'),
    ('/calendar/world-clock.html', '세계 시계', '🌏', '#EEF4FF'),
]


def key(path):
    return path.strip('/').replace('/', '-').replace('.html', '') or 'home'
