import java.io.Serializable;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

public class Filmovi2_V1 {

	public static void main(String[] args) {
		String fileName = "title.basics.tsv";
		int startYear = 1900;
		int endYear = 2020;

		long start = System.currentTimeMillis();

		SparkConf conf = new SparkConf().setAppName("filmovi2").setMaster("local");

		try (JavaSparkContext context = new JavaSparkContext(conf);) {

			JavaRDD<String> lines = context.textFile(fileName);

			JavaRDD<Film> map = lines.map(s -> new Film(s));
			JavaRDD<Film> filter = map.filter(film -> film.year > startYear && film.year < endYear);
			JavaRDD<List<YTC>> listaGodKat = filter.map(film -> {
				List<YTC> list = new LinkedList<>();
				for (String categorie : film.categories) {
					list.add(new YTC(film.year + "-" + categorie, 1));
				}
				return list;
			});

			JavaRDD<YTC> flatMap = listaGodKat.flatMap(elem -> elem.iterator());
			Map<String, Long> countByValue = flatMap.map(elem -> elem.type).countByValue();
			for (java.util.Map.Entry<String, Long> entry : countByValue.entrySet()) {
				System.out.println(entry.getKey() + "," + entry.getValue());
			}

		}
		long end = System.currentTimeMillis();
		System.out.printf("start: %d, end: %d, time: %d\n", start, end, end - start);
	}

	@SuppressWarnings("serial")
	public static class YTC implements Serializable {

		String type;
		int count;

		public YTC(String type, int count) {
			super();
			this.type = type;
			this.count = count;
		}

		@Override
		public String toString() {
			return type + ", " + count;
		}

	}

	@SuppressWarnings("serial")
	public static class Film implements Serializable {

		int year;
		String[] categories;

		public Film(String s) {
			try {
				String[] data = s.split("\t");
				year = Integer.parseInt(data[5]);
				categories = data[8].split(",");
			} catch (Exception e) {
				year = -1;
				categories = new String[0];
			}

		}

	}
}
