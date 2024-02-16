import asyncio
import willofsteel

client = willofsteel.Wrapper("WoS-fod8k80ps3-gjor-ljgl-nbet-59xmhr1o6i")
def main():
    player = client.get_player()
    print(player)
    alliance = client.get_alliance()
    print(alliance)


main()