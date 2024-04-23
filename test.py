for ant in Ant.instances:
    shift = ant.cell_size / 2
    ant.find_and_interact(Berry.instances, "{} нашёл {}", set_stuck=False)
    ant.find_and_interact(Web.instanses, "{} нашёл паутину :( {}", set_stuck=True)
    ant.find_and_interact(Spider.instances, "{} нашёл паука :( {}", set_stuck=True)
    if ant.selected or ant.stuck or abs(ant.x - x) > shift or abs(ant.y - y) > shift:
        ant.deselect()
        self.itemconfig(ant.obj, image=ant.get_image())
        continue
    ant.select()
    self.itemconfig(ant.obj, image=ant.get_image())
    print(ant.name, 'выбран')
    self.bind('<Button-1>', lambda e, arg=ant: self.ant_direction(e, arg))
    if not ant.carries:
        for berry in Berry.instances:
            if berry.has_matching_indexes_with(ant) and not berry.taken:
                self.btn_list.append(TakeButton(self, "Взять", ant.x, ant.y))
                break
        hexes_indexes_nearby = self.list_of_hexes_indexes_nearby(ant)
        for ant_friend in Ant.instances:
            if (ant_friend.i, ant_friend.j) in hexes_indexes_nearby and ant_friend.stuck:
                print("Друг в беде!", ant_friend.name, ant_friend.i, ant_friend.j)

    else:
        if self.hexes_dict.get((ant.i, ant.j)).is_anthill:
            self.btn_list.append(DropButton(self, 'Бросить', ant.x, ant.y))
            print(ant.name, 'дома с ягодкой')
    break
