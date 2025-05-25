import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import asyncio

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
            self.hp = await self.dis_hp()
            self.attack = await self.dis_attack()
            self.defense = await self.dis_defense()

        return f"Pokémonunuzun ismi: {self.name} \nHP: {self.hp} \nAttack: {self.attack} \nDefense: {self.defense}"  # Pokémon adını içeren dizeyi döndürür

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['sprites']['other']["official-artwork"]["front_default"]  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür
    
    async def dis_hp(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['stats'][0]["base_stat"]  #  Pokémon adını döndürme
                else:
                    return 50  # İstek başarısız olursa varsayılan adı döndürür
    async def dis_attack(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['stats'][1]["base_stat"]  #  Pokémon adını döndürme
                else:
                    return 0  # İstek başarısız olursa varsayılan adı döndürür
    async def dis_defense(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['stats'][2]["base_stat"]  #  Pokémon adını döndürme
                else:
                    return 0  # İstek başarısız olursa varsayılan adı döndürür
    
    async def war(self, enemy):
        if isinstance(enemy, Wizard):
            luck = random.randint(1, 5)
            if luck == 1:
                return f"{self.name}, {enemy.name} isimli pokemona saldırdı! \n{enemy.name} kalkan kullandı!"
        damage = round(self.attack * (1 - enemy.defense / (enemy.defense + 100)))
        if enemy.hp > damage:
            enemy.hp -= damage
            return f"{self.name}, {enemy.name} isimli pokemona saldırdı! {damage} verdi! \n{enemy.name} isimli pokemonun kalan canı: {enemy.hp}"
        else:
            return f"{self.name}, {enemy.name} isimli pokemona saldırdı! {enemy.name} yenildi!"

class Fighter(Pokemon):
    async def war(self, enemy):
        bonus_attack = random.randint(0,10)
        self.attack += bonus_attack
        result = await super().war(enemy)
        self.attack -= bonus_attack
        return f"Bonus attack puanı: {bonus_attack} \n{result}"

class Wizard(Pokemon):
    pass

if __name__ == "__main__":
    async def pokemonn():
        pikapika = Fighter("SL")
        pikapika2 = Fighter("Yoruko")
        print(await pikapika.info())
        print("--------------------------------------------")
        print(await pikapika2.info())
        print("--------------------------------------------")
        print(await pikapika.war(pikapika2))
        print("--------------------------------------------")
        print(await pikapika2.war(pikapika))
    asyncio.run(pokemonn())