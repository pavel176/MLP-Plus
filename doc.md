## Правила
- Каждая команда идён с новой строчки
- Аргументы разделяются пробелами
- Названия начинающиеся на $ или & являются системными
- Тела функции определяются табуляцией
## Инструкции
### Ввод и вывод
<0> = <1>[<2>]
> read <0> <1> <2>

<0>[<1>] = <2>
> write <2> <0> <1>

print <0>
> print <0>
> 
> printflash $printflash

print <0> <1>
> print <0>
> 
> printflash <1>

clear_display <0> <1> <2>
> draw clear <0> <1> <2> 0 0 0

set_color <0> <1> <2>
> draw color <0> <1> <2> 0 0 0

set_color <0>
> draw col <0> 0 0 0 0 0

set_width <0>
> draw stroke <0> 0 0 0 0 0

draw_line <0> <1> <2> <3>
> draw line <0> <1> <2> <3> 0 0

draw_line_rect <0> <1> <2> <3>
> draw lineRect <0> <1> <2> <3> 0 0

draw_line <0> <1> <2> <3> <4>
> draw poly <0> <1> <2> <3> <4> 0

draw_line_rect <0> <1> <2> <3> <4>
> draw linePoly <0> <1> <2> <3> <4> 0

draw_triangle <0> <1> <2> <3> <4> <5>
> draw triangle <0> <1> <2> <3> <4> <5>

draw_image <0> <1> <2> <3> <4>
> draw image <0> <1> <2> <3> <4> 0

display_update <0>
> drawflush <0>

### Управление блоками

<0> = link <1>
> getlink <0> <1>

<0>.build.enabled <1>
> control enabled <0> <1> 0 0 0

<0>.build.shoot_to_point <1> <2>
> control shoot <0> <1> <2> 1 0

<0>.build.shoot_to_point <1> <2> <3>
> control shoot <0> <1> <2> <3> 0

<0>.build.shoot_to_enemy <1>
> control shootp <0> <1> 1 0 0

<0>.build.shoot_to_enemy <1> <2>
> control shootp <0> <1> <2> 0 0

<0>.build.config <1>
> control config <0> <1> 1 0 0

<0>.build.config <1>
> control color <0> <1> 1 0 0

<0>.build.config <1> <2> <3>
> packcolor $temp_a <1> <2> <3>
>
> control color <0> $temp_a 0 0 0








