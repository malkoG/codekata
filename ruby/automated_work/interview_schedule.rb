# coding: utf-8
a=[]
b=Hash.new(0)
c=Hash.new(0)
d=Hash.new(0)
keys = []
vals = []
list = []
num = 0

while(line=gets)
  a << [num, line]
  num += 1
end

a.each do |x|
  num = x[0]
  x = x[1].split "\t"
  x = [x[1], (x[7].split ',').map(&:strip)]
  str = "#{num}, #{x[0]}"
  x[-1].each do |y|
    if b[y]==0
      b[y] = [str]
      c[y] = [str]
    else
      b[y] << str
      c[y] << str
    end

  end
  list << str
end

b.sort_by {|k, v| k}.each do |k, v|
  keys << k.rjust(20)
  vals << v.map {|x| x.rjust(20) }
end

c = c.sort_by {|x,y| y.size}

c = c.map do |k, v|
  v = v.select {|x| d[x] == 0 }
  v.each {|x| d[x] += 1}
  [k, v]
end

result_keys = []
result_vals = []

c = c.sort_by {|k, v| k }.each do |x, y|
  result_keys << x.rjust(20)
  result_vals << y.map {|r| r.rjust(20) }
  y.each {|x| list.delete x}
end

count = vals.map {|x| x.size }.max
keys = keys[0..-2].join

puts "날짜별 희망인원"
puts keys
puts vals = vals[0..-2].map {|x| count >= x.size ? x + ["".rjust(20)] * (count-x.size) : x }.transpose.map {|x| x.join }

result_count = result_vals.map {|x| x.size }.max
result_keys = result_keys[0..-2].join

puts "배치결과"
puts result_keys
puts result_vals = result_vals[0..-2].map {|x| count >= x.size ? x + ["".rjust(20)] * (count-x.size) : x }.transpose.map {|x| x.join }

puts "잔여명단"
puts list.join ','
